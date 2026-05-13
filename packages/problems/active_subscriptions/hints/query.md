```sql
SELECT sub_id, customer_id, plan, start_date, end_date
FROM subscriptions
WHERE start_date <= '2024-06-15'
  AND end_date >= '2024-06-15'
ORDER BY sub_id
```
