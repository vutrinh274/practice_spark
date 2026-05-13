# Solution: SQL

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
        event_id,
        user_id,
        page,
        event_time,
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
    SUM(new_session_flag) OVER (
        PARTITION BY user_id
        ORDER BY event_time
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS session_id
FROM flagged
ORDER BY user_id, event_time
```

## Explanation

1. **`lagged` CTE** — pull the previous event time for each user using `LAG`.
2. **`flagged` CTE** — compare the current and previous timestamps. If the gap exceeds 1800 seconds (30 min) or there is no previous event (start of user's history), mark `new_session_flag = 1`.
3. **Final SELECT** — `SUM(new_session_flag)` as a running total gives each event a session counter. Because the first event always gets flag 1, session IDs naturally start at 1.
