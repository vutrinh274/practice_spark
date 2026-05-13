Once you have the `price_tier` column, select only the required columns and order by `price` ascending.

```sql
SELECT product_id, product_name, price,
       CASE WHEN price < 50 THEN 'Budget'
            WHEN price < 500 THEN 'Mid-range'
            ELSE 'Premium' END AS price_tier
FROM products
ORDER BY price
```
