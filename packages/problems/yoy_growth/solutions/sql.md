## SQL Solution

```sql
WITH lagged AS (
    SELECT category,
           year,
           revenue,
           LAG(revenue) OVER (PARTITION BY category ORDER BY year) AS prev_revenue
    FROM annual_revenue
)
SELECT category,
       year,
       revenue,
       ROUND((revenue - prev_revenue) / prev_revenue * 100, 2) AS yoy_growth_pct
FROM lagged
ORDER BY category, year
```

**Why it works:**
- The CTE adds `prev_revenue` via LAG — NULL for the first year per category
- Division by NULL propagates NULL, so the first year's growth is NULL automatically
- `ROUND(..., 2)` formats the growth percentage
- The CTE improves readability vs repeating the LAG expression twice
