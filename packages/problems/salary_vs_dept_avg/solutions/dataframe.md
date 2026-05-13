## DataFrame API Solution

```python
# F (pyspark.sql.functions) and Window are pre-imported

w = Window.partitionBy("department")

result = (
    df
    .withColumn("dept_avg_salary", F.round(F.avg("salary").over(w), 2))
    .withColumn("diff_from_avg", F.round(F.col("salary") - F.avg("salary").over(w), 2))
    .select("employee_id", "name", "department", "salary", "dept_avg_salary", "diff_from_avg")
    .orderBy("department", "employee_id")
)
```

**Why it works:**
- `Window.partitionBy("department")` groups rows by department without an ORDER BY (no ranking needed here)
- `F.avg("salary").over(w)` computes the department average for each row
- Two `withColumn` calls add the derived columns before the final select
