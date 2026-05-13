## DataFrame API Solution

```python
# F (pyspark.sql.functions) and Window are pre-imported
# employees and departments are available as variables

result = (
    employees
    .join(departments, on="department_id", how="outer")
    .withColumn("department_id", F.coalesce(
        employees["department_id"], departments["department_id"]
    ))
    .select("employee_id", "name", "department_id", "department_name", "budget")
    .orderBy(F.asc_nulls_last("department_id"), F.asc_nulls_last("employee_id"))
)
```

**Why it works:**
- `how="outer"` is the full outer join
- `F.coalesce(...)` picks the non-NULL department_id from either side
- `F.asc_nulls_last(...)` — Spark-specific function to sort NULLs last
