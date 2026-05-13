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
