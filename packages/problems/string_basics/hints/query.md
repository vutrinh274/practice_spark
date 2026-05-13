`INITCAP` handles Title Case for you — no need to manually capitalize:

```sql
SELECT customer_id,
       INITCAP(CONCAT(TRIM(first_name), ' ', TRIM(last_name))) AS full_name,
       LOWER(TRIM(email)) AS email,
       INITCAP(TRIM(city)) AS city
FROM customers
ORDER BY customer_id
```
