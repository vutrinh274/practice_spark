```sql
SELECT sale_date, amount,
       ROUND(AVG(amount) OVER (ORDER BY sale_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW), 2) AS rolling_avg_7d
FROM daily_sales
ORDER BY sale_date
```
