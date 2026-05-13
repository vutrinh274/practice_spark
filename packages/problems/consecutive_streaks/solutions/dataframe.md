# Solution: DataFrame API

```python
# F (pyspark.sql.functions) and Window are pre-imported

w = Window.partitionBy("employee_id").orderBy("attendance_date")

result = (
    attendance
    .filter(F.col("status") == "Present")
    .withColumn("rn", F.row_number().over(w))
    .withColumn("grp", F.date_sub(F.col("attendance_date"), F.col("rn")))
    .groupBy("employee_id", "grp")
    .agg(F.count("*").alias("streak_len"))
    .groupBy("employee_id")
    .agg(F.max("streak_len").alias("max_streak"))
    .orderBy("employee_id")
)

result.show()
```

## Explanation

- Filter to `Present` rows only — absent days are irrelevant to streaks.
- `row_number().over(w)` numbers the present days per employee in date order.
- `date_sub(attendance_date, rn)` produces the same anchor for all days in a contiguous island (the "islands and gaps" trick).
- The first `groupBy` counts each island's size; the second finds the maximum across all islands per employee.
