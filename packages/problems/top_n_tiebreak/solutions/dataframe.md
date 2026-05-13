# Solution: DataFrame API

```python
# F (pyspark.sql.functions) and Window are pre-imported

w = Window.partitionBy("department").orderBy(
    F.col("salary").desc(),
    F.col("employee_id").asc(),
)

result = (
    employees
    .withColumn("row_num", F.row_number().over(w))
    .filter(F.col("row_num") <= 2)
    .select("department", "employee_id", "name", "salary", "row_num")
    .orderBy("department", "row_num")
)

result.show()
```

## Explanation

- The window is partitioned by `department` and ordered by `salary DESC, employee_id ASC`, fully resolving any ties.
- `row_number()` assigns 1, 2, 3, ... to employees within each department — no ties, no gaps.
- Filtering `row_num <= 2` keeps exactly the top two earners per department.
- `select` and `orderBy` produce the clean, deterministic output required.
