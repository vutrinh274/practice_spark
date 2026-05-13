#!/usr/bin/env python3
"""
Validate all problems by submitting their reference solutions to the API.
Usage: python scripts/validate_problems.py [problem_id]
"""
import sys
import yaml
import requests
from pathlib import Path

API_URL = "http://localhost:8000"
PROBLEMS_DIR = Path(__file__).parent.parent / "packages" / "problems"

def get_sql_solution(problem_dir: Path) -> str | None:
    path = problem_dir / "solutions" / "sql.md"
    if not path.exists():
        return None
    content = path.read_text()
    blocks = list(__import__("re").finditer(r"```sql\n(.*?)```", content, __import__("re").DOTALL))
    return blocks[0].group(1).strip() if blocks else None

def get_dataframe_solution(problem_dir: Path) -> str | None:
    path = problem_dir / "solutions" / "dataframe.md"
    if not path.exists():
        return None
    content = path.read_text()
    blocks = list(__import__("re").finditer(r"```python\n(.*?)```", content, __import__("re").DOTALL))
    return blocks[0].group(1).strip() if blocks else None

def strip_comments(code: str) -> str:
    return "\n".join(
        line for line in code.splitlines()
        if not line.strip().startswith("#")
    ).strip()

def validate_problem(problem_id: str) -> dict:
    problem_dir = PROBLEMS_DIR / problem_id
    yaml_path = problem_dir / "problem.yaml"
    if not yaml_path.exists():
        return {"problem_id": problem_id, "error": "problem.yaml not found"}

    results = {"problem_id": problem_id, "sql": None, "dataframe": None}

    # Test SQL solution
    sql_code = get_sql_solution(problem_dir)
    if sql_code:
        resp = requests.post(f"{API_URL}/submit", json={
            "problem_id": problem_id,
            "mode": "sql",
            "code": sql_code
        })
        data = resp.json()
        results["sql"] = "✅ PASS" if data.get("passed") else f"❌ FAIL: {data.get('feedback', '')[:100]}"
    else:
        results["sql"] = "⚠️  No SQL solution found"

    # Test DataFrame solution
    df_code = get_dataframe_solution(problem_dir)
    if df_code:
        clean_code = strip_comments(df_code)
        resp = requests.post(f"{API_URL}/submit", json={
            "problem_id": problem_id,
            "mode": "dataframe",
            "code": clean_code
        })
        data = resp.json()
        results["dataframe"] = "✅ PASS" if data.get("passed") else f"❌ FAIL: {data.get('feedback', '')[:100]}"
    else:
        results["dataframe"] = "⚠️  No DataFrame solution found"

    return results

def main():
    registry_path = PROBLEMS_DIR / "registry.yaml"
    registry = yaml.safe_load(registry_path.read_text())

    if len(sys.argv) > 1:
        problem_ids = [sys.argv[1]]
    else:
        problem_ids = [
            entry["path"].lstrip("./")
            for entry in registry.get("problems", [])
        ]

    print(f"\n{'─' * 60}")
    print(f"Validating {len(problem_ids)} problem(s) against {API_URL}")
    print(f"{'─' * 60}\n")

    passed = 0
    failed = 0
    for pid in problem_ids:
        result = validate_problem(pid)
        sql_status = result.get("sql", "—")
        df_status = result.get("dataframe", "—")
        print(f"[{pid}]")
        print(f"  SQL:       {sql_status}")
        print(f"  DataFrame: {df_status}")
        print()
        if "PASS" in str(sql_status) and "PASS" in str(df_status):
            passed += 1
        elif "error" in result:
            failed += 1
        elif "FAIL" in str(sql_status) or "FAIL" in str(df_status):
            failed += 1

    print(f"{'─' * 60}")
    print(f"Results: {passed} fully passing, {failed} with failures")
    print(f"{'─' * 60}\n")

if __name__ == "__main__":
    main()
