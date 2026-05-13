## SQL Solution

```sql
SELECT product_id, product_name, SIZE(SPLIT(tags, ',')) AS tag_count
FROM products_with_arrays
ORDER BY tag_count DESC, product_id
```

**Why it works:**
- `SPLIT(tags, ',')` converts the comma-separated string to an array
- `SIZE(...)` returns the number of elements in that array — equivalent to `len()` in Python
- No `GROUP BY` is needed because we compute a scalar per row
- The dual `ORDER BY` gives a stable sort when products tie on `tag_count`
