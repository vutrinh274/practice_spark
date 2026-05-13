## SQL Solution

```sql
SELECT customer_id FROM orders WHERE product = 'Laptop'
INTERSECT
SELECT customer_id FROM orders WHERE product = 'Phone'
ORDER BY customer_id
```

**Why it works:**
- Each subquery returns the set of customers who bought that product
- `INTERSECT` keeps only customers present in both sets
- Alternative using GROUP BY + HAVING also works — both are valid Spark SQL
