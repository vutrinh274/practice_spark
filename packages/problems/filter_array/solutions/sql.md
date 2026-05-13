## SQL Solution

```sql
SELECT user_id, name
FROM user_interests
WHERE ARRAY_CONTAINS(SPLIT(interests, ','), 'Technology')
ORDER BY user_id
```

**Why it works:**
- `SPLIT(interests, ',')` converts the comma-separated string into an array
- `ARRAY_CONTAINS(array, 'Technology')` checks for an exact match of the element in the array
- Only rows where the condition is true are returned
- `ORDER BY user_id` gives a deterministic result
