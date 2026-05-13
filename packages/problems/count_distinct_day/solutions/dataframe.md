## DataFrame API Solution

```python
# F (pyspark.sql.functions) and Window are pre-imported

result = (
    df
    .groupBy("event_date")
    .agg(
        F.countDistinct("user_id").alias("distinct_users"),
        F.count("*").alias("total_events")
    )
    .orderBy("event_date")
)
```

**Why it works:**
- `.groupBy("event_date")` groups all events by day
- `F.countDistinct("user_id")` is the DataFrame equivalent of `COUNT(DISTINCT user_id)`
- `F.count("*")` counts all rows regardless of duplicates
