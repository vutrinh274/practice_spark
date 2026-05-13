## SQL Solution

```sql
SELECT product_id, product_name, EXPLODE(SPLIT(tags, ',')) AS tag
FROM products_with_arrays
ORDER BY product_id, tag
```

**Why it works:**
- `SPLIT(tags, ',')` converts the comma-separated string into an array of strings
- `EXPLODE(...)` expands the array — one output row per element
- The result is aliased as `tag` for a clean column name
- Ordering by `product_id` then `tag` gives a stable, deterministic result
