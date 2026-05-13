# Approach

## Step-by-Step Plan

1. **Create a window** partitioned by `user_id`, ordered by `event_time`.
2. **Get the previous event time** using `LAG(event_time, 1)` over the window.
3. **Compute gap in seconds**: `UNIX_TIMESTAMP(event_time) - UNIX_TIMESTAMP(prev_time)`.
4. **Flag new sessions**: `CASE WHEN gap > 1800 OR prev_time IS NULL THEN 1 ELSE 0 END`.
5. **Running sum of flags** over the same window gives a session counter per user (starts at 1 for the first event).
6. **Select** the required columns and order the result.

## Pseudocode

```
w = PARTITION BY user_id ORDER BY event_time

prev_time  = LAG(event_time, 1) OVER w
gap_secs   = UNIX_TIMESTAMP(event_time) - UNIX_TIMESTAMP(prev_time)
new_flag   = CASE WHEN gap_secs > 1800 OR prev_time IS NULL THEN 1 ELSE 0 END
session_id = SUM(new_flag) OVER w   -- running total within user
```

Note: `SUM(new_flag) OVER w` with no explicit ROWS clause defaults to RANGE UNBOUNDED PRECEDING to CURRENT ROW, which is what you want for a running total.
