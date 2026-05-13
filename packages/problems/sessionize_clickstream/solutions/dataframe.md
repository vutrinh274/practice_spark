# Solution: DataFrame API

```python
# F (pyspark.sql.functions) and Window are pre-imported

# Window for LAG and running SUM — ordered by event_time within each user
w = Window.partitionBy("user_id").orderBy("event_time")
w_running = Window.partitionBy("user_id").orderBy("event_time").rowsBetween(
    Window.unboundedPreceding, Window.currentRow
)

result = (
    clickstream
    .withColumn("prev_time", F.lag("event_time", 1).over(w))
    .withColumn(
        "gap_secs",
        F.unix_timestamp("event_time") - F.unix_timestamp("prev_time")
    )
    .withColumn(
        "new_flag",
        F.when(
            F.col("prev_time").isNull() | (F.col("gap_secs") > 1800), 1
        ).otherwise(0)
    )
    .withColumn("session_id", F.sum("new_flag").over(w_running))
    .select("event_id", "user_id", "page", "event_time", "session_id")
    .orderBy("user_id", "event_time")
)

result.show()
```

## Explanation

- `lag("event_time", 1).over(w)` retrieves the timestamp of the immediately preceding event per user.
- The gap in seconds is computed by converting both timestamps via `unix_timestamp`.
- `new_flag` is 1 when the gap exceeds 30 minutes or there is no prior event.
- `F.sum("new_flag").over(w_running)` accumulates the flags into a monotonically increasing session counter. Because every user's first event receives flag 1, session IDs start at 1.
