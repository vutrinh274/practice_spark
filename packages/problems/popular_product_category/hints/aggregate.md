First join and aggregate total quantity per product:

```sql
SELECT p.category, p.product_name, SUM(s.quantity) AS total_quantity
FROM products p
JOIN sales s ON p.product_id = s.product_id
GROUP BY p.category, p.product_name
```
