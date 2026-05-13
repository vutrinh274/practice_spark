## SQL Solution

```sql
SELECT product_id, product_name, category, total_sales
FROM products
ORDER BY total_sales DESC
LIMIT 5
```

**Why it works:**
- `ORDER BY total_sales DESC` sorts highest to lowest
- `LIMIT 5` keeps only the first 5 rows after sorting
