```sql
SELECT
  contact_id,
  name,
  phone AS original_phone,
  CONCAT(
    SUBSTRING(digits, 1, 3), '-',
    SUBSTRING(digits, 4, 3), '-',
    SUBSTRING(digits, 7, 4)
  ) AS standardized_phone
FROM (
  SELECT *, REGEXP_REPLACE(phone, '[^0-9]', '') AS digits
  FROM contacts
)
ORDER BY contact_id
```
