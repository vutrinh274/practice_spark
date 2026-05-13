## SQL Solution

```sql
SELECT user_id, ARRAY_JOIN(ARRAY_SORT(COLLECT_SET(TRIM(item))), ',') AS all_items
FROM (
  SELECT user_id, EXPLODE(SPLIT(items, ',')) AS item
  FROM user_purchases
)
GROUP BY user_id
ORDER BY user_id
```

**Why it works:**
- `EXPLODE(SPLIT(items, ','))` splits comma-separated items into individual rows
- `COLLECT_SET(TRIM(item))` deduplicates items (set semantics)
- `ARRAY_SORT(...)` ensures consistent ordering
- `ARRAY_JOIN(..., ',')` converts to a string for reliable comparison
