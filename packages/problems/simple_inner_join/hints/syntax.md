Join on the shared key `customer_id`:

```sql
SELECT o.order_id, c.name, c.city, o.amount
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
```
