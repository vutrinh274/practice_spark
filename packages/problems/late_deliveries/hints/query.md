```sql
SELECT order_id, customer_id, promised_days, actual_days,
       actual_days - promised_days AS days_late
FROM (
  SELECT *, DATEDIFF(delivery_date, order_date) AS actual_days
  FROM orders
) t
WHERE actual_days > promised_days
ORDER BY days_late DESC
```
