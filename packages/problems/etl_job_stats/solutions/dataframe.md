## DataFrame API Solution

```python
# F (pyspark.sql.functions) and Window are pre-imported

agg_df = (
    df
    .withColumn(
        "duration_seconds",
        F.unix_timestamp(F.col("end_time")) - F.unix_timestamp(F.col("start_time"))
    )
    .groupBy("pipeline")
    .agg(
        F.count("job_id").alias("total_runs"),
        F.round(
            F.sum(F.when(F.col("status") == "success", 1).otherwise(0)) * 100.0 / F.count("job_id"),
            2
        ).alias("success_rate"),
        F.round(F.avg("duration_seconds"), 2).alias("avg_duration_seconds"),
        F.round(F.avg("rows_processed"), 2).alias("avg_rows_processed"),
    )
)

w = Window.orderBy(F.col("success_rate").desc())

result = (
    agg_df
    .withColumn("rank", F.dense_rank().over(w))
    .select("pipeline", "total_runs", "success_rate", "avg_duration_seconds", "avg_rows_processed", "rank")
    .orderBy("rank")
)
```

**Why it works:**
- `F.unix_timestamp` converts a timestamp string to epoch seconds; subtraction gives duration
- `F.when(...).otherwise(0)` is the DataFrame equivalent of `CASE WHEN`
- `F.dense_rank().over(w)` applies dense ranking over the unpartitioned window ordered by success rate descending
- The intermediate `agg_df` is computed first so the window function can reference the already-aggregated `success_rate` column
