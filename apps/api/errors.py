SPARK_ERROR_MAP = {
    "UNRESOLVED_COLUMN": "Column not found. Check your column names for typos.",
    "UNRESOLVED_COLUMN.WITH_SUGGESTION": "Column not found. Check your column names for typos.",
    "TABLE_OR_VIEW_NOT_FOUND": "Table or view not found. Use the table name provided in the problem.",
    "PARSE_SYNTAX_ERROR": "SQL syntax error. Check your query syntax.",
    "DATATYPE_MISMATCH": "Type mismatch. You may be comparing or combining incompatible column types.",
    "MISSING_GROUP_BY": "Missing GROUP BY. You're selecting a non-aggregated column alongside an aggregate function — add it to GROUP BY.",
    "AMBIGUOUS_COLUMN_OR_FIELD": "Ambiguous column name. Qualify it with the table name (e.g. table.column).",
    "UNRESOLVED_ROUTINE": "Unknown function. Check the function name for typos.",
    "DIVIDE_BY_ZERO": "Division by zero detected in your query.",
    "UNSUPPORTED_SUBQUERY_EXPRESSION_CATEGORY": "Unsupported subquery. Try rewriting using a JOIN or window function.",
}

DATAFRAME_NAME_ERRORS = {
    "F": "Use `F.sum()`, `F.col()`, etc. — `pyspark.sql.functions` is available as `F`.",
    "Window": "`Window` is available directly — use `Window.partitionBy(...).orderBy(...)`.",
    "col": "Use `F.col('column_name')` instead of `col(...)` — functions are accessed via `F`.",
    "lit": "Use `F.lit(value)` instead of `lit(...)` — functions are accessed via `F`.",
    "sum": "Use `F.sum('column')` instead of `sum(...)` — Spark functions are accessed via `F`.",
    "count": "Use `F.count('column')` instead of `count(...)` — Spark functions are accessed via `F`.",
    "avg": "Use `F.avg('column')` instead of `avg(...)` — Spark functions are accessed via `F`.",
    "when": "Use `F.when(condition, value)` instead of `when(...)` — functions are accessed via `F`.",
    "spark": "`spark` is not available in DataFrame mode. All tables are available as variables by name (e.g. `orders`, `customers`) — use them directly.",
}

FALLBACK = "Something went wrong while running your query. Check your code and try again."


def friendly_error(exc: Exception) -> str:
    msg = str(exc)

    # NameError in DataFrame mode — guide user to use F.xxx
    if isinstance(exc, NameError):
        # Extract the name from "name 'xxx' is not defined"
        import re
        match = re.search(r"name '(\w+)' is not defined", msg)
        if match:
            name = match.group(1)
            if name in DATAFRAME_NAME_ERRORS:
                return DATAFRAME_NAME_ERRORS[name]
            return f"Name `{name}` is not defined. In DataFrame mode, use `F.{name}()` for Spark functions, or check your variable names."

    for code, template in SPARK_ERROR_MAP.items():
        if code in msg:
            return template
    return FALLBACK
