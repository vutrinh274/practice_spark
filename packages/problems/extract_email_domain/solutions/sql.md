## SQL Solution

```sql
SELECT user_id, name, email, REGEXP_EXTRACT(email, '@(.+)$', 1) AS domain
FROM users
ORDER BY user_id
```

**Why it works:**
- `REGEXP_EXTRACT(email, '@(.+)$', 1)` applies the regex `@(.+)$` to the `email` column.
- The `@` matches the literal at-sign; `(.+)$` captures one or more characters until end of string — the domain.
- Capture group index `1` returns just the domain portion without the `@`.
