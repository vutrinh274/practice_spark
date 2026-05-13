Using INTERSECT:

```sql
SELECT customer_id FROM orders WHERE product = 'Laptop'
INTERSECT
SELECT customer_id FROM orders WHERE product = 'Phone'
ORDER BY customer_id
```

Using GROUP BY + HAVING:

```sql
SELECT customer_id
FROM orders
WHERE product IN ('Laptop', 'Phone')
GROUP BY customer_id
HAVING COUNT(DISTINCT product) = 2
ORDER BY customer_id
```
