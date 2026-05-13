## SQL Solution

```sql
SELECT c.customer_id, c.name, c.city,
       SUM(o.quantity * p.price) AS total_revenue
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN products p ON o.product_id = p.product_id
GROUP BY c.customer_id, c.name, c.city
ORDER BY total_revenue DESC
```

**Why it works:**
- Two `JOIN`s link `orders` to `customers` and `products` using their shared keys
- `quantity * price` computes revenue per order line
- `SUM(...)` aggregates total revenue per customer
- `GROUP BY` includes all non-aggregated columns from the SELECT
