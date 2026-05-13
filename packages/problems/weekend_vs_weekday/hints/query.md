```sql
SELECT
  CASE WHEN DAYOFWEEK(sale_date) IN (1, 7) THEN 'Weekend' ELSE 'Weekday' END AS day_type,
  SUM(amount) AS total_revenue,
  COUNT(*) AS num_sales
FROM sales
GROUP BY day_type
ORDER BY day_type
```
