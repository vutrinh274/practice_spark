After the LEFT JOIN, filter where `order_id IS NULL` — these are the customers with no matching order:

```sql
SELECT c.customer_id, c.name, c.city, c.signup_date
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL
ORDER BY c.customer_id
```
