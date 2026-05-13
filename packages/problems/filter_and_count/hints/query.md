Filter first with `WHERE country = 'USA'`, then aggregate:

```sql
SELECT country,
       COUNT(DISTINCT customer_id) AS distinct_customers,
       SUM(amount) AS total_revenue
FROM orders
WHERE country = 'USA'
GROUP BY country
```
