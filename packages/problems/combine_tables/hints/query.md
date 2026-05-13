```sql
SELECT * FROM orders_2023
UNION ALL
SELECT * FROM orders_2024
ORDER BY order_id
```
