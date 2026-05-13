## SQL Solution

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

**Why it works:**
- The inner query adds `actual_days` via `DATEDIFF(delivery_date, order_date)` — note end date comes first
- The outer `WHERE actual_days > promised_days` keeps only late deliveries
- `days_late` is computed as the difference between actual and promised, showing how many extra days were taken
- `ORDER BY days_late DESC` surfaces the most-delayed orders first
