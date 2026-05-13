## SQL Solution

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

**Why it works:**
- The inner query uses `REGEXP_REPLACE(phone, '[^0-9]', '')` to strip every non-digit character, leaving exactly 10 digits in `digits`.
- `SUBSTRING(digits, 1, 3)` — first 3 digits (area code).
- `SUBSTRING(digits, 4, 3)` — next 3 digits (exchange).
- `SUBSTRING(digits, 7, 4)` — final 4 digits (subscriber number).
- `CONCAT(...)` assembles them with `-` separators into `XXX-XXX-XXXX`.
