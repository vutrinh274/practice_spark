## SQL Solution

```sql
WITH stats AS (
    SELECT
        percentile_approx(amount, 0.25) AS q1,
        percentile_approx(amount, 0.75) AS q3
    FROM transactions
)
SELECT t.transaction_id, t.amount
FROM transactions t
CROSS JOIN stats
WHERE t.amount BETWEEN (q1 - 1.5 * (q3 - q1)) AND (q3 + 1.5 * (q3 - q1))
ORDER BY t.transaction_id
```

**Why it works:**
- The CTE computes Q1 and Q3 across all rows once
- `CROSS JOIN stats` makes the percentile values available to every row
- The `BETWEEN` clause applies the IQR fence: lower = Q1 - 1.5*IQR, upper = Q3 + 1.5*IQR
- Rows outside the fence (outliers) are excluded
