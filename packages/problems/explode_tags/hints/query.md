```sql
SELECT product_id, product_name, EXPLODE(SPLIT(tags, ',')) AS tag
FROM products_with_arrays
ORDER BY product_id, tag
```
