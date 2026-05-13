```sql
SELECT user_id,
       MIN(event_date) AS first_event,
       MAX(event_date) AS last_event,
       COUNT(*) AS total_events
FROM user_events
GROUP BY user_id
ORDER BY user_id
```
