```sql
SELECT
  customer_id,
  name,
  CONCAT(SUBSTRING(email, 1, 3), '***@', REGEXP_EXTRACT(email, '@(.+)$', 1)) AS masked_email,
  CONCAT('***-***-', SUBSTRING(phone, LENGTH(phone) - 3, 4)) AS masked_phone
FROM customers
ORDER BY customer_id
```
