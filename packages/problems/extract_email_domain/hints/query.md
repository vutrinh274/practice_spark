```sql
SELECT user_id, name, email, REGEXP_EXTRACT(email, '@(.+)$', 1) AS domain
FROM users
ORDER BY user_id
```
