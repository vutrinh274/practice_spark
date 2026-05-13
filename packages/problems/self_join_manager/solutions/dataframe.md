## DataFrame API Solution

```python
# F (pyspark.sql.functions) and Window are pre-imported

managers = df.select(
    F.col("employee_id").alias("manager_id"),
    F.col("name").alias("manager_name")
)

result = (
    df
    .join(managers, on="manager_id", how="left")
    .select("employee_id", "name", "department", "manager_name")
    .orderBy("employee_id")
)
```

**Why it works:**
- Create a `managers` DataFrame with just `manager_id` and `manager_name`
- Left join the original `df` on `manager_id`
- Employees without a manager get NULL for `manager_name`
