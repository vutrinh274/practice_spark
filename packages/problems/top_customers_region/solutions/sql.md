## SQL Solution

```sql
WITH ranked AS (
    SELECT region,
           customer_id,
           name,
           total_spend,
           RANK() OVER (PARTITION BY region ORDER BY total_spend DESC) AS rank
    FROM customers
)
SELECT region, customer_id, name, total_spend, rank
FROM ranked
WHERE rank <= 2
ORDER BY region, rank
```

**Why it works:**
- The CTE assigns a rank within each region, 1 being the highest spender
- `WHERE rank <= 2` keeps only the top 2 customers per region
- Window function results cannot be filtered in the same query level — a CTE or subquery is required
- `ORDER BY region, rank` gives a clean region-by-region view of the top customers
