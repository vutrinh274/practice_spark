```sql
SELECT p.product_id, p.product_name, p.category, p.price
FROM products p
LEFT JOIN sales s ON p.product_id = s.product_id
WHERE s.sale_id IS NULL
ORDER BY p.product_id
```
