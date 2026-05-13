## SQL Solution

```sql
SELECT sub_id, customer_id, plan, start_date, end_date
FROM subscriptions
WHERE start_date <= '2024-06-15'
  AND end_date >= '2024-06-15'
ORDER BY sub_id
```

**Why it works:**
- ISO 8601 date strings sort lexicographically the same as chronologically, so string comparison is valid here
- `start_date <= '2024-06-15'` ensures the subscription had already started
- `end_date >= '2024-06-15'` ensures the subscription had not yet expired
- Both conditions together select only subscriptions that overlap the target date
