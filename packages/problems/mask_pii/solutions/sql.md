## SQL Solution

```sql
SELECT
  customer_id,
  name,
  CONCAT(SUBSTRING(email, 1, 3), '***@', REGEXP_EXTRACT(email, '@(.+)$', 1)) AS masked_email,
  CONCAT('***-***-', SUBSTRING(phone, LENGTH(phone) - 3, 4)) AS masked_phone
FROM customers
ORDER BY customer_id
```

**Why it works:**
- `SUBSTRING(email, 1, 3)` takes the first 3 characters of the local part.
- `REGEXP_EXTRACT(email, '@(.+)$', 1)` captures the domain after the `@`.
- `CONCAT(...)` assembles the masked email: `ali***@gmail.com`.
- For the phone (format `XXX-XXX-XXXX`), `SUBSTRING(phone, LENGTH(phone) - 3, 4)` extracts the last 4 digits.
- `CONCAT('***-***-', ...)` builds the masked phone: `***-***-4567`.
