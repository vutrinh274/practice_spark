## SQL Solution

```sql
SELECT event_date,
       COUNT(DISTINCT user_id) AS distinct_users,
       COUNT(*) AS total_events
FROM user_events
GROUP BY event_date
ORDER BY event_date
```

**Why it works:**
- `GROUP BY event_date` produces one row per day
- `COUNT(DISTINCT user_id)` counts each user only once per day, even if they triggered multiple events
- `COUNT(*)` counts every event row including duplicates
