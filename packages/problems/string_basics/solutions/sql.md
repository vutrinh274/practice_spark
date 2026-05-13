## SQL Solution

```sql
SELECT customer_id,
       INITCAP(CONCAT(TRIM(first_name), ' ', TRIM(last_name))) AS full_name,
       LOWER(TRIM(email)) AS email,
       INITCAP(TRIM(city)) AS city
FROM customers
ORDER BY customer_id
```

**Why it works:**
- `TRIM()` removes leading/trailing whitespace
- `CONCAT(..., ' ', ...)` joins first and last name with a space
- `INITCAP()` applies Title Case — a Spark SQL function not available in all SQL dialects
- `LOWER()` lowercases the email
