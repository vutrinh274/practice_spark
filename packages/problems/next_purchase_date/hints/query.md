```sql
SELECT purchase_id, customer_id, purchase_date,
       LEAD(purchase_date) OVER (PARTITION BY customer_id ORDER BY purchase_date) AS next_purchase_date
FROM purchases
ORDER BY customer_id, purchase_date
```
