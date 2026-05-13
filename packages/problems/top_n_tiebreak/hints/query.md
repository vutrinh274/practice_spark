# Query Hint

## SQL Skeleton

```sql
WITH ranked AS (
    SELECT
        department,
        employee_id,
        name,
        salary,
        ROW_NUMBER() OVER (
            PARTITION BY department
            ORDER BY salary DESC, employee_id ASC
        ) AS row_num
    FROM employees
)
SELECT department, employee_id, name, salary, row_num
FROM ranked
WHERE row_num <= 2
ORDER BY department, row_num
```

## DataFrame Skeleton

```python
w = Window.partitionBy("department").orderBy(
    F.col("salary").desc(), F.col("employee_id").asc()
)

result = (
    df.withColumn("row_num", F.row_number().over(w))
      .filter(F.col("row_num") <= 2)
      .select("department", "employee_id", "name", "salary", "row_num")
      .orderBy("department", "row_num")
)
```
