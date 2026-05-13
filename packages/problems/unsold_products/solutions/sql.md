## SQL Solution

```sql
SELECT p.product_id, p.product_name, p.category, p.price
FROM products p
LEFT JOIN sales s ON p.product_id = s.product_id
WHERE s.sale_id IS NULL
ORDER BY p.product_id
```

**Why it works:**
- `LEFT JOIN` keeps all products, filling NULL for sale columns with no match
- `WHERE s.sale_id IS NULL` keeps only products never sold
