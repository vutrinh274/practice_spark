```sql
SELECT sale_date,
       SUM(amount) AS total_amount,
       COUNT(*) AS num_transactions
FROM sales
GROUP BY sale_date
ORDER BY sale_date
```
