```sql
SELECT product_id, product_name, SIZE(SPLIT(tags, ',')) AS tag_count
FROM products_with_arrays
ORDER BY tag_count DESC, product_id
```
