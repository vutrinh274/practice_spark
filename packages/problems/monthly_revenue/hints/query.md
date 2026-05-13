```sql
SELECT DATE_FORMAT(order_date, 'yyyy-MM') AS month,
       SUM(amount) AS total_revenue,
       COUNT(*) AS num_orders
FROM orders
GROUP BY DATE_FORMAT(order_date, 'yyyy-MM')
ORDER BY month
```
