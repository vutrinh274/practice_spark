## SQL Solution

```sql
SELECT sale_date,
       amount,
       ROUND(AVG(amount) OVER (ORDER BY sale_date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW), 2) AS rolling_avg_7d
FROM daily_sales
ORDER BY sale_date
```

**Why it works:**
- `ORDER BY sale_date` orders rows chronologically within the window
- `ROWS BETWEEN 6 PRECEDING AND CURRENT ROW` defines a physical frame of up to 7 rows
- `AVG(amount)` over that frame computes the rolling average
- `ROUND(..., 2)` rounds to 2 decimal places
- For the first 6 days, the window shrinks to whatever rows are available
