## SQL Solution

```sql
SELECT sale_date,
       SUM(amount) AS total_amount,
       COUNT(*) AS num_transactions
FROM sales
GROUP BY sale_date
ORDER BY sale_date
```

**Why it works:**
- `GROUP BY sale_date` collapses all rows for the same date into one
- `SUM(amount)` totals the sales for that day
- `COUNT(*)` counts how many individual transactions happened
