```sql
SELECT category, year, revenue,
       ROUND(
           (revenue - LAG(revenue) OVER (PARTITION BY category ORDER BY year))
           / LAG(revenue) OVER (PARTITION BY category ORDER BY year) * 100,
           2
       ) AS yoy_growth_pct
FROM annual_revenue
ORDER BY category, year
```
