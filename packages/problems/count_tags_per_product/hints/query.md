```sql
SELECT product_id, product_name, COUNT(*) AS tag_count
FROM (
  SELECT product_id, product_name, EXPLODE(SPLIT(tags, ',')) AS tag
  FROM products
)
GROUP BY product_id, product_name
ORDER BY tag_count DESC, product_id
```
