## SQL Solution

```sql
SELECT
  CASE WHEN DAYOFWEEK(sale_date) IN (1, 7) THEN 'Weekend' ELSE 'Weekday' END AS day_type,
  SUM(amount) AS total_revenue,
  COUNT(*) AS num_sales
FROM sales
GROUP BY CASE WHEN DAYOFWEEK(sale_date) IN (1, 7) THEN 'Weekend' ELSE 'Weekday' END
ORDER BY day_type
```

**Why it works:**
- `DAYOFWEEK` returns 1 for Sunday and 7 for Saturday in Spark SQL
- The `CASE WHEN ... IN (1, 7)` expression captures both weekend days in a single condition
- `GROUP BY` on the expression collapses all sales into two buckets
- `SUM` and `COUNT` compute the totals for each bucket
