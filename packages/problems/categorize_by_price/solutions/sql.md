## SQL Solution

```sql
SELECT product_id, product_name, price,
       CASE
         WHEN price < 50 THEN 'Budget'
         WHEN price < 500 THEN 'Mid-range'
         ELSE 'Premium'
       END AS price_tier
FROM products
ORDER BY price
```

**Why it works:**
- `CASE WHEN` evaluates conditions in order — first match wins
- `price < 500` in the second condition implicitly means `>= 50` since the first condition already handles `< 50`
- `ELSE 'Premium'` catches everything `>= 500`
