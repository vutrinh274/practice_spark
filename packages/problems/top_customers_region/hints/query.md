```sql
WITH ranked AS (
    SELECT region, customer_id, name, total_spend,
           RANK() OVER (PARTITION BY region ORDER BY total_spend DESC) AS rank
    FROM customers
)
SELECT region, customer_id, name, total_spend, rank
FROM ranked
WHERE rank <= 2
ORDER BY region, rank
```
