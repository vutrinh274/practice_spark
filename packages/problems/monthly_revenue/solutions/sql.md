## SQL Solution

```sql
SELECT DATE_FORMAT(order_date, 'yyyy-MM') AS month,
       SUM(amount) AS total_revenue,
       COUNT(*) AS num_orders
FROM orders
GROUP BY DATE_FORMAT(order_date, 'yyyy-MM')
ORDER BY month
```

**Why it works:**
- `DATE_FORMAT(order_date, 'yyyy-MM')` extracts year-month as a string
- `GROUP BY` on that string collapses all orders in the same month
- `SUM` and `COUNT` aggregate revenue and order count
