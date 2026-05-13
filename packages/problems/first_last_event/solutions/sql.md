## SQL Solution

```sql
SELECT user_id,
       MIN(event_date) AS first_event,
       MAX(event_date) AS last_event,
       COUNT(*) AS total_events
FROM user_events
GROUP BY user_id
ORDER BY user_id
```

**Why it works:**
- `GROUP BY user_id` produces one row per user
- `MIN(event_date)` finds the earliest date in the group
- `MAX(event_date)` finds the latest date in the group
- `COUNT(*)` tallies all events for that user
