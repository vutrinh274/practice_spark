# Solution: SQL

```sql
WITH stage_map AS (
    SELECT 'view'     AS stage, 1 AS stage_order UNION ALL
    SELECT 'cart'     AS stage, 2 AS stage_order UNION ALL
    SELECT 'checkout' AS stage, 3 AS stage_order UNION ALL
    SELECT 'purchase' AS stage, 4 AS stage_order
),
counts AS (
    SELECT
        event_type AS stage,
        COUNT(DISTINCT user_id) AS users_reached
    FROM user_events
    GROUP BY event_type
)
SELECT
    c.stage,
    s.stage_order,
    c.users_reached
FROM counts c
JOIN stage_map s ON c.stage = s.stage
ORDER BY s.stage_order
```

## Explanation

1. **`stage_map` CTE** — an inline lookup table that assigns a numeric order to each stage name.
2. **`counts` CTE** — aggregates `COUNT(DISTINCT user_id)` per `event_type`, giving the number of unique users who performed each action at least once.
3. **Final SELECT** — joins the two CTEs on stage name, selects the required columns, and orders by `stage_order` so the funnel progresses from top to bottom.
