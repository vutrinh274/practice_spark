## DataFrame API Solution

```python
# F (pyspark.sql.functions) and Window are pre-imported

result = (
    df
    .fillna({"department": "Unknown", "salary": 0})
    .filter(F.col("salary") > 0)
    .select("employee_id", "name", "department", "salary")
    .orderBy("employee_id")
)
```

**Why it works:**
- `.fillna({"department": "Unknown", "salary": 0})` replaces NULLs per column
- `.filter(F.col("salary") > 0)` removes rows with no salary
- `.select(...)` ensures correct column order
