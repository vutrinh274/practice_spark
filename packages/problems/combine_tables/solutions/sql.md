## SQL Solution

```sql
SELECT * FROM orders_2023
UNION ALL
SELECT * FROM orders_2024
ORDER BY order_id
```

**Why it works:**
- `UNION ALL` stacks rows from both tables without removing duplicates
- `UNION` (without ALL) would deduplicate — not what we want here since all orders are unique
- `ORDER BY order_id` sorts the combined result
