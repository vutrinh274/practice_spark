Add `LIMIT 5` at the end of your query to keep only the top 5 rows. In DataFrame API use `.limit(5)`.

```sql
SELECT * FROM products
ORDER BY total_sales DESC
LIMIT 5
```
