```sql
SELECT customer_id,
       SUM(CASE WHEN status = 'completed' THEN amount ELSE 0 END) AS completed_revenue,
       SUM(CASE WHEN status = 'cancelled' THEN amount ELSE 0 END) AS cancelled_revenue,
       COUNT(*) AS total_orders
FROM orders
GROUP BY customer_id
ORDER BY customer_id
```
