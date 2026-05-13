## SQL Solution

```sql
SELECT country,
       COUNT(DISTINCT customer_id) AS distinct_customers,
       SUM(amount) AS total_revenue
FROM orders
WHERE country = 'USA'
GROUP BY country
```

**Why it works:**
- `WHERE country = 'USA'` filters before aggregation
- `COUNT(DISTINCT customer_id)` counts unique customers only
- `SUM(amount)` totals revenue for filtered rows
