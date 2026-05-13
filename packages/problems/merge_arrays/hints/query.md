```sql
SELECT user_id, ARRAY_SORT(COLLECT_LIST(DISTINCT item)) AS all_items
FROM (
  SELECT user_id, EXPLODE(SPLIT(items, ',')) AS item
  FROM user_purchases
)
GROUP BY user_id
ORDER BY user_id
```
