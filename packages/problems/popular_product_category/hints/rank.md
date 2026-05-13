Then use `RANK() OVER (PARTITION BY category ORDER BY total_quantity DESC)` to rank within each category, and filter `rank = 1`:

```sql
SELECT category, product_name, total_quantity
FROM (
  SELECT category, product_name, total_quantity,
         RANK() OVER (PARTITION BY category ORDER BY total_quantity DESC) AS rank
  FROM (... aggregation ...)
)
WHERE rank = 1
```
