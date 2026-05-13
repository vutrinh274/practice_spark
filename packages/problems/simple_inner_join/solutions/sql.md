## SQL Solution

```sql
SELECT o.order_id, c.name, c.city, o.amount
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.status = 'completed'
ORDER BY o.order_id
```

**Why it works:**
- `JOIN customers c ON o.customer_id = c.customer_id` links orders to their customer
- `WHERE o.status = 'completed'` filters out pending and cancelled orders
- Note: customer Eve (id=5) has no orders so she doesn't appear — that's INNER JOIN behavior
