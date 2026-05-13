The aggregate function you need is `SUM(amount)`. Alias the result column as `total_amount`.

```sql
SELECT customer_id, SUM(amount) AS total_amount
FROM data
GROUP BY ...
```
