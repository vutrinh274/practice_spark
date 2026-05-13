## SQL Solution

```sql
SELECT purchase_id,
       customer_id,
       purchase_date,
       LEAD(purchase_date) OVER (PARTITION BY customer_id ORDER BY purchase_date) AS next_purchase_date
FROM purchases
ORDER BY customer_id, purchase_date
```

**Why it works:**
- `PARTITION BY customer_id` keeps each customer's rows in an isolated window
- `ORDER BY purchase_date` arranges rows chronologically within each partition
- `LEAD(purchase_date)` returns the value from the next row; returns NULL for the last row in each partition
