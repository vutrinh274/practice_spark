## DataFrame API Solution

```python
# F (pyspark.sql.functions) and Window are pre-imported

result = (
    df
    .withColumn("month", F.date_format(F.col("activity_date"), "yyyy-MM"))
    .groupBy("month")
    .agg(F.countDistinct("user_id").alias("active_users"))
    .orderBy("month")
)
```

**Why it works:**
- `F.date_format(...)` creates a `yyyy-MM` string column for grouping
- `F.countDistinct("user_id")` counts each user_id only once per month group
- `.orderBy("month")` sorts the final result chronologically
