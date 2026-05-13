## SQL Solution

```sql
SELECT
  user_id,
  signup_date,
  first_purchase_date,
  DATEDIFF(first_purchase_date, signup_date) AS days_to_purchase
FROM (
  SELECT
    user_id,
    MAX(CASE WHEN event_type = 'signup' THEN event_date END) AS signup_date,
    MAX(CASE WHEN event_type = 'first_purchase' THEN event_date END) AS first_purchase_date
  FROM user_events
  GROUP BY user_id
) t
ORDER BY user_id
```

**Why it works:**
- The inner query pivots the long-format table into one row per user using conditional `MAX`
- `DATEDIFF(end, start)` computes the integer number of days between two date strings
- The outer `ORDER BY user_id` sorts the final result
