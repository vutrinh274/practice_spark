## SQL Solution

```sql
SELECT product_id, product_name, COUNT(*) AS tag_count
FROM (
  SELECT product_id, product_name, EXPLODE(SPLIT(tags, ',')) AS tag
  FROM products
)
GROUP BY product_id, product_name
ORDER BY tag_count DESC, product_id
```

**Why it works:**
- `SPLIT(tags, ',')` converts the comma-separated string into an array.
- `EXPLODE(...)` turns each array element into a separate row so `COUNT(*)` can tally them.
- Ordering by `tag_count DESC, product_id ASC` produces a deterministic result.
