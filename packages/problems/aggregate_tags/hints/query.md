```sql
SELECT product_id, product_name, COLLECT_LIST(tag) AS tags
FROM products
GROUP BY product_id, product_name
ORDER BY product_id
```
