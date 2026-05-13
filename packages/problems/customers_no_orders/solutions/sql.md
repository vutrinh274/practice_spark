## SQL Solution

```sql
SELECT c.customer_id, c.name, c.city, c.signup_date
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL
ORDER BY c.customer_id
```

**Why it works:**
- `LEFT JOIN` keeps all customers, filling NULL for order columns when no match exists
- `WHERE o.order_id IS NULL` keeps only customers with no matching order — the anti-join pattern
