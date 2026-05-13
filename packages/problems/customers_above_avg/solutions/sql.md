## SQL Solution

```sql
WITH customer_totals AS (
    SELECT customer_id, SUM(amount) AS total_spend
    FROM orders
    GROUP BY customer_id
)
SELECT customer_id, total_spend
FROM customer_totals
WHERE total_spend > (SELECT AVG(total_spend) FROM customer_totals)
ORDER BY total_spend DESC
```

**Why it works:**
- The CTE computes total spend per customer once
- The scalar subquery `(SELECT AVG(total_spend) FROM customer_totals)` returns the average of the per-customer totals
- `WHERE total_spend > ...` filters to only above-average customers
