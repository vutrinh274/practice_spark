## SQL Solution

```sql
SELECT product_id, product_name, ARRAY_JOIN(ARRAY_SORT(COLLECT_LIST(tag)), ',') AS tags
FROM products
GROUP BY product_id, product_name
ORDER BY product_id
```

**Why it works:**
- `COLLECT_LIST(tag)` aggregates all tags into an array
- `ARRAY_SORT(...)` sorts the array for consistent ordering
- `ARRAY_JOIN(..., ',')` converts the array to a comma-separated string for comparison
