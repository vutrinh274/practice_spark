## SQL Solution

```sql
SELECT customer_id, order_date, amount,
       SUM(amount) OVER (
         PARTITION BY customer_id
         ORDER BY order_date
         ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
       ) AS running_total
FROM orders
ORDER BY customer_id, order_date
```

**Why it works:**
- `PARTITION BY customer_id` resets the running total per customer
- `ORDER BY order_date` ensures the sum accumulates chronologically
- `ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW` explicitly includes all rows from the start of the partition to the current row
