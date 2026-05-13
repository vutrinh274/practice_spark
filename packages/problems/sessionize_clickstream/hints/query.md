# Query Hint

## SQL Skeleton

```sql
WITH lagged AS (
    SELECT
        event_id,
        user_id,
        page,
        event_time,
        LAG(event_time) OVER (PARTITION BY user_id ORDER BY event_time) AS prev_time
    FROM clickstream
),
flagged AS (
    SELECT
        *,
        CASE
            WHEN prev_time IS NULL
                 OR UNIX_TIMESTAMP(event_time) - UNIX_TIMESTAMP(prev_time) > 1800
            THEN 1
            ELSE 0
        END AS new_session_flag
    FROM lagged
)
SELECT
    event_id,
    user_id,
    page,
    event_time,
    SUM(new_session_flag) OVER (PARTITION BY user_id ORDER BY event_time) AS session_id
FROM flagged
ORDER BY user_id, event_time
```

## DataFrame Skeleton

```python
w_lag = Window.partitionBy("user_id").orderBy("event_time")

df = df.withColumn("prev_time", F.lag("event_time", 1).over(w_lag))
df = df.withColumn(
    "gap_secs",
    F.unix_timestamp("event_time") - F.unix_timestamp("prev_time")
)
df = df.withColumn(
    "new_flag",
    F.when(F.col("prev_time").isNull() | (F.col("gap_secs") > 1800), 1).otherwise(0)
)
w_sum = Window.partitionBy("user_id").orderBy("event_time").rowsBetween(
    Window.unboundedPreceding, Window.currentRow
)
df = df.withColumn("session_id", F.sum("new_flag").over(w_sum))
```
