import asyncio
import os
import threading
import time
from pyspark.sql import SparkSession, DataFrame
from pyspark.testing.utils import assertDataFrameEqual
from loader import get_problem, Problem

SPARK_CONNECT_URL = os.getenv("SPARK_CONNECT_URL", "sc://localhost:15002")
SPARK_PROBLEMS_DIR = os.getenv("SPARK_PROBLEMS_DIR", "/problems")
JOB_TIMEOUT = 60  # seconds

# Per-user session pool
# Anonymous users share a single session; authenticated users get their own
_SESSION_TTL = 30 * 60  # 30 minutes idle before eviction
_user_sessions: dict[str, dict] = {}  # {user_id: {"session": SparkSession, "last_used": float}}
_sessions_lock = threading.Lock()
_ANON_KEY = "__anon__"


def _create_session() -> SparkSession:
    return SparkSession.builder.remote(SPARK_CONNECT_URL).create()


def _get_session(user_id: str | None) -> SparkSession:
    """Return session for user_id, or shared anon session. Creates if needed."""
    key = user_id if user_id else _ANON_KEY
    with _sessions_lock:
        entry = _user_sessions.get(key)
        if entry:
            entry["last_used"] = time.time()
            return entry["session"]
        session = _create_session()
        _user_sessions[key] = {"session": session, "last_used": time.time()}
        return session


def _evict_idle_sessions():
    """Remove sessions idle longer than TTL. Call periodically."""
    now = time.time()
    with _sessions_lock:
        to_evict = [k for k, v in _user_sessions.items() if now - v["last_used"] > _SESSION_TTL]
        for k in to_evict:
            _user_sessions.pop(k, None)
    if to_evict:
        print(f"[sessions] Evicted {len(to_evict)} idle sessions")

# SQL patterns that should never be executed by users
_BLOCKED_SQL_PATTERNS = [
    # System catalog access
    "information_schema", "sys.", "system.", "spark_catalog",
    # Admin commands
    "show tables", "show databases", "show schemas",
    "describe ", "explain ", "set ", "reset ",
    # Write operations
    "insert into", "delete from", "drop table", "drop view",
    "create table", "create view", "alter table", "truncate ",
    # File system access
    "load data", "into outfile", "into dumpfile",
]


def _validate_schema_only(user_df: DataFrame, expected_df: DataFrame) -> None:
    user_cols = {f.name.lower(): f.dataType for f in user_df.schema.fields}
    expected_cols = {f.name.lower(): f.dataType for f in expected_df.schema.fields}
    missing = set(expected_cols) - set(user_cols)
    extra = set(user_cols) - set(expected_cols)
    type_mismatches = {
        col: (str(user_cols[col]), str(expected_cols[col]))
        for col in set(user_cols) & set(expected_cols)
        if user_cols[col] != expected_cols[col]
    }
    errors = []
    if missing:
        errors.append(f"Missing columns: {', '.join(sorted(missing))}")
    if extra:
        errors.append(f"Unexpected columns: {', '.join(sorted(extra))}")
    if type_mismatches:
        for col, (got, want) in type_mismatches.items():
            errors.append(f"Column '{col}': expected type {want}, got {got}")
    if errors:
        raise AssertionError("\n".join(errors))


def _validate_row_count(user_df: DataFrame, expected_df: DataFrame) -> None:
    user_count = user_df.count()
    expected_count = expected_df.count()
    if user_count != expected_count:
        raise AssertionError(
            f"Row count mismatch: expected {expected_count} rows, got {user_count} rows."
        )


VALIDATORS = {
    "dataframe_equal": lambda u, e: assertDataFrameEqual(u, e, checkRowOrder=False),
    "dataframe_equal_ordered": lambda u, e: assertDataFrameEqual(u, e, checkRowOrder=True),
    "schema_only": _validate_schema_only,
    "row_count": _validate_row_count,
}


def _get_fresh_session_for(user_id: str | None) -> SparkSession:
    """Force-create a new session for user, replacing any existing one."""
    key = user_id if user_id else _ANON_KEY
    session = _create_session()
    with _sessions_lock:
        _user_sessions[key] = {"session": session, "last_used": time.time()}
    return session


def _load_datasets(problem: Problem, spark: SparkSession) -> dict[str, DataFrame]:
    frames = {}
    for ds in problem.datasets:
        if ds.source == "csv":
            df = spark.read.option("header", True).option("inferSchema", True)\
                .option("quote", '"').option("escape", '"').csv(ds.path)
        elif ds.source == "parquet":
            df = spark.read.parquet(ds.path)
        elif ds.source == "json":
            df = spark.read.option("multiLine", True).json(ds.path)
        else:
            raise ValueError(f"Unsupported source: {ds.source}")
        df.createOrReplaceTempView(ds.name)
        frames[ds.name] = df
    return frames


def _load_expected(problem: Problem, spark: SparkSession) -> DataFrame:
    spark_path = f"{SPARK_PROBLEMS_DIR}/{problem.id}/expected.csv"
    # inferSchema=False prevents date strings like '2024-01' being parsed as timestamps
    return spark.read.option("header", True).option("inferSchema", False)\
        .option("quote", '"').option("escape", '"').csv(spark_path)


def _check_sql(code: str) -> str | None:
    lower = code.lower()
    for pattern in _BLOCKED_SQL_PATTERNS:
        if pattern in lower:
            return f"Query contains disallowed pattern: '{pattern}'"
    return None


def _run_sql(code: str, spark: SparkSession) -> DataFrame:
    return spark.sql(code)


def _run_dataframe(code: str, frames: dict[str, DataFrame]) -> DataFrame:
    from pyspark.sql import functions as F
    from pyspark.sql.window import Window
    local_vars = {"df": next(iter(frames.values())), **frames, "F": F, "Window": Window}
    exec(code, {"__builtins__": __builtins__}, local_vars)  # AST check is the guard, not exec
    result = local_vars.get("result")
    if result is None:
        raise ValueError("Your code must assign the final DataFrame to a variable named 'result'.")
    return result


def _coerce_types(user_df: DataFrame, expected_df: DataFrame) -> DataFrame:
    """Cast expected_df columns to match user_df types where column names align."""
    from pyspark.sql import functions as F
    user_types = {f.name: f.dataType for f in user_df.schema.fields}
    casts = []
    for field in expected_df.schema.fields:
        if field.name in user_types and field.dataType != user_types[field.name]:
            casts.append(F.col(field.name).cast(user_types[field.name]).alias(field.name))
        else:
            casts.append(F.col(field.name))
    return expected_df.select(casts)


def _friendly_diff(user_df: DataFrame, expected_df: DataFrame, raw_error: str) -> str:
    messages = []

    # Schema check — uses schema metadata, no collect needed
    user_cols = {f.name for f in user_df.schema.fields}
    expected_cols = {f.name for f in expected_df.schema.fields}
    missing = expected_cols - user_cols
    extra = user_cols - expected_cols
    if missing:
        messages.append(f"Missing columns: {', '.join(sorted(missing))}")
    if extra:
        messages.append(f"Unexpected columns: {', '.join(sorted(extra))}")
    if missing or extra:
        return "\n".join(messages)

    # Collect once, reuse for both count and row diff
    user_rows = [tuple(r) for r in user_df.collect()]
    expected_rows = [tuple(r) for r in expected_df.collect()]

    if len(user_rows) != len(expected_rows):
        messages.append(f"Wrong number of rows: got {len(user_rows)}, expected {len(expected_rows)}")
        return "\n".join(messages)

    user_set = set(user_rows)
    expected_set = set(expected_rows)
    missing_rows = expected_set - user_set
    extra_rows = user_set - expected_set
    cols = [f.name for f in expected_df.schema.fields]
    if missing_rows:
        messages.append("Expected rows not in your result (first 3):")
        for row in list(missing_rows)[:3]:
            messages.append(f"  {dict(zip(cols, row))}")
    if extra_rows:
        messages.append("Rows in your result not expected (first 3):")
        for row in list(extra_rows)[:3]:
            messages.append(f"  {dict(zip(cols, row))}")

    return "\n".join(messages) if messages else raw_error


def _validate(user_df: DataFrame, expected_df: DataFrame, problem: Problem) -> dict:
    strategy = problem.validation.strategy
    validator = VALIDATORS.get(strategy)
    if validator is None:
        return {"passed": False, "feedback": f"Unknown validation strategy: {strategy}"}
    if problem.validation.type_coerce:
        expected_df = _coerce_types(user_df, expected_df)
    try:
        validator(user_df, expected_df)
        return {"passed": True, "feedback": "Correct!"}
    except AssertionError as e:
        return {"passed": False, "feedback": _friendly_diff(user_df, expected_df, str(e))}


async def validate_sql(problem_id: str, code: str) -> dict:
    """Run Spark analyzer on the query without executing it. Returns {valid, error}."""
    loop = asyncio.get_event_loop()

    def _run(spark=None):
        problem = get_problem(problem_id)
        spark = spark or _get_session(None)
        _load_datasets(problem, spark)

        sql_error = _check_sql(code)
        if sql_error:
            return {"valid": False, "error": sql_error}

        try:
            spark.sql(code).schema
            return {"valid": True, "error": None}
        except Exception as e:
            from errors import friendly_error
            return {"valid": False, "error": friendly_error(e)}

    def _run_with_retry():
        try:
            return _run()
        except Exception as e:
            if "SESSION_CLOSED" in str(e) or "INVALID_HANDLE" in str(e):
                return _run(_get_fresh_session_for(None))
            raise

    return await asyncio.wait_for(loop.run_in_executor(None, _run_with_retry), timeout=60)


async def execute_submission(problem_id: str, mode: str, code: str, user_id: str | None = None) -> dict:
    loop = asyncio.get_event_loop()

    def _run(spark=None):
        problem = get_problem(problem_id)
        spark = spark or _get_session(user_id)
        frames = _load_datasets(problem, spark)
        expected_df = _load_expected(problem, spark)

        if mode == "sql":
            sql_error = _check_sql(code)
            if sql_error:
                return {"passed": False, "feedback": sql_error}
            user_df = _run_sql(code, spark)
        else:
            user_df = _run_dataframe(code, frames)

        validation = _validate(user_df, expected_df, problem)

        # Collect result rows (limit 100, note if truncated)
        total = user_df.count()
        rows_df = user_df.limit(100).toPandas()
        validation["columns"] = list(rows_df.columns)
        # Convert to JSON-safe list — replace NaN/NaT with None
        import math
        def safe(v):
            if v is None:
                return None
            try:
                if math.isnan(float(v)):
                    return None
            except (TypeError, ValueError):
                pass
            return v
        validation["rows"] = [[safe(v) for v in row] for row in rows_df.values.tolist()]
        validation["total_rows"] = total
        validation["truncated"] = total > 100

        return validation

    def _run_with_retry():
        try:
            return _run()
        except Exception as e:
            if "SESSION_CLOSED" in str(e) or "INVALID_HANDLE" in str(e):
                return _run(_get_fresh_session_for(user_id))
            raise

    return await asyncio.wait_for(loop.run_in_executor(None, _run_with_retry), timeout=JOB_TIMEOUT)
