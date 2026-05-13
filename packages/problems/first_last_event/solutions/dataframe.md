## DataFrame API Solution

```python
# F (pyspark.sql.functions) and Window are pre-imported

result = (
    df
    .groupBy("user_id")
    .agg(
        F.min("event_date").alias("first_event"),
        F.max("event_date").alias("last_event"),
        F.count("*").alias("total_events")
    )
    .orderBy("user_id")
)
```

**Why it works:**
- `.groupBy("user_id")` groups all rows per user
- `F.min` and `F.max` find the date boundaries within each group
- `F.count("*")` counts all rows in the group
