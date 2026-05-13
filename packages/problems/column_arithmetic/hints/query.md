Build the derived columns step by step:

```sql
SELECT product_id, product_name,
       ROUND(price * (1 - discount_pct / 100.0), 2) AS discounted_price,
       ROUND(price * (1 - discount_pct / 100.0) * quantity, 2) AS total_revenue
FROM products
ORDER BY total_revenue DESC
```
