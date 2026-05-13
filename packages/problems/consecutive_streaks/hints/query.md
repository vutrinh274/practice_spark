# Query Hint

## SQL Skeleton

```sql
WITH present AS (
    SELECT employee_id, attendance_date
    FROM attendance
    WHERE status = 'Present'
),
numbered AS (
    SELECT
        employee_id,
        attendance_date,
        ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY attendance_date) AS rn
    FROM present
),
islands AS (
    SELECT
        employee_id,
        DATE_SUB(attendance_date, rn) AS grp,
        COUNT(*) AS streak_len
    FROM numbered
    GROUP BY employee_id, DATE_SUB(attendance_date, rn)
)
SELECT employee_id, MAX(streak_len) AS max_streak
FROM islands
GROUP BY employee_id
ORDER BY employee_id
```

## DataFrame Skeleton

```python
w = Window.partitionBy("employee_id").orderBy("attendance_date")

present = df.filter(F.col("status") == "Present")

result = (
    present
    .withColumn("rn", F.row_number().over(w))
    .withColumn("grp", F.date_sub(F.col("attendance_date"), F.col("rn")))
    .groupBy("employee_id", "grp")
    .agg(F.count("*").alias("streak_len"))
    .groupBy("employee_id")
    .agg(F.max("streak_len").alias("max_streak"))
    .orderBy("employee_id")
)
```
