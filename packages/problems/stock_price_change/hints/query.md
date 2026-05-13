```sql
SELECT stock, price_date, close_price,
       close_price - LAG(close_price) OVER (PARTITION BY stock ORDER BY price_date) AS price_change
FROM stock_prices
ORDER BY stock, price_date
```
