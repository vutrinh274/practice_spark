```sql
SELECT rep_id, name, region, total_sales,
       ROUND(PERCENT_RANK() OVER (PARTITION BY region ORDER BY total_sales DESC), 2) AS pct_rank,
       NTILE(4) OVER (PARTITION BY region ORDER BY total_sales DESC) AS quartile
FROM sales_reps
ORDER BY region, total_sales DESC
```
