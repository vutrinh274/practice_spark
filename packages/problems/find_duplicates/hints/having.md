Filter groups using `HAVING COUNT(*) > 1` — this keeps only emails that appear more than once.

```sql
SELECT email, COUNT(*) AS count
FROM users
GROUP BY email
HAVING COUNT(*) > 1
```
