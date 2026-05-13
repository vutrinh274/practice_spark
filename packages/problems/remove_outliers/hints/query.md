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
