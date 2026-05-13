## SQL Solution

```sql
SELECT product_id, product_name,
       ROUND(price * (1 - discount_pct / 100.0), 2) AS discounted_price,
       ROUND(price * (1 - discount_pct / 100.0) * quantity, 2) AS total_revenue
FROM products
ORDER BY total_revenue DESC
```

**Why it works:**
- `discount_pct / 100.0` uses float division to avoid integer truncation
- `price * (1 - ...)` computes the discounted price per unit
- Multiply by `quantity` for total revenue
- `ROUND(..., 2)` rounds to 2 decimal places
