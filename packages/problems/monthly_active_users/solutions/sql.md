## SQL Solution

```sql
SELECT DATE_FORMAT(activity_date, 'yyyy-MM') AS month,
       COUNT(DISTINCT user_id) AS active_users
FROM user_activity
GROUP BY DATE_FORMAT(activity_date, 'yyyy-MM')
ORDER BY month
```

**Why it works:**
- `DATE_FORMAT(activity_date, 'yyyy-MM')` converts a date string into a `yyyy-MM` month key
- `COUNT(DISTINCT user_id)` counts each user only once per month, even if they had multiple activities
- `GROUP BY` on the formatted month collapses all rows in the same month
