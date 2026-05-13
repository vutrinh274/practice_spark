```sql
SELECT DATE_FORMAT(activity_date, 'yyyy-MM') AS month,
       COUNT(DISTINCT user_id) AS active_users
FROM user_activity
GROUP BY DATE_FORMAT(activity_date, 'yyyy-MM')
ORDER BY month
```
