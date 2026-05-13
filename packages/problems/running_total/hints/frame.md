Explicitly define the window frame to include all rows from the start up to the current row:

```sql
SUM(amount) OVER (
  PARTITION BY customer_id
  ORDER BY order_date
  ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
) AS running_total
```
