## SQL Solution

```sql
SELECT rep_id,
       name,
       region,
       total_sales,
       ROUND(PERCENT_RANK() OVER (PARTITION BY region ORDER BY total_sales DESC), 2) AS pct_rank,
       NTILE(4) OVER (PARTITION BY region ORDER BY total_sales DESC) AS quartile
FROM sales_reps
ORDER BY region, total_sales DESC
```

**Why it works:**
- Both window functions share the same partition and ordering
- `PERCENT_RANK()` gives 0.0 for the top performer and 1.0 for the lowest within each region
- `NTILE(4)` assigns quartile labels 1–4 where 1 is the top quartile
- `ROUND(..., 2)` formats the percent rank to 2 decimal places
