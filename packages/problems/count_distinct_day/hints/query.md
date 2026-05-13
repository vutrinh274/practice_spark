```sql
SELECT event_date,
       COUNT(DISTINCT user_id) AS distinct_users,
       COUNT(*) AS total_events
FROM user_events
GROUP BY event_date
ORDER BY event_date
```
