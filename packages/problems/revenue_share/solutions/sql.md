## SQL Solution

```sql
SELECT category, total_revenue,
       ROUND(total_revenue * 100.0 / SUM(total_revenue) OVER (), 2) AS revenue_pct
FROM (
  SELECT category, SUM(amount) AS total_revenue
  FROM orders
  GROUP BY category
)
ORDER BY revenue_pct DESC
```

**Why it works:**
- Inner query computes total revenue per category
- `SUM(total_revenue) OVER ()` — window with no PARTITION gets the grand total
- Dividing by grand total gives the percentage share
