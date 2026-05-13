## SQL Solution

```sql
SELECT stock,
       price_date,
       close_price,
       close_price - LAG(close_price) OVER (PARTITION BY stock ORDER BY price_date) AS price_change
FROM stock_prices
ORDER BY stock, price_date
```

**Why it works:**
- `PARTITION BY stock` keeps each stock's rows in its own window
- `ORDER BY price_date` ensures the lag looks at the chronologically previous row
- `LAG(close_price)` fetches the previous row's close price (defaults to NULL for the first row)
- Subtracting gives the daily change; NULL subtraction yields NULL for the first day
