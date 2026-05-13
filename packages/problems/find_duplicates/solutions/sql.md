## SQL Solution

```sql
SELECT email, COUNT(*) AS count
FROM users
GROUP BY email
HAVING COUNT(*) > 1
ORDER BY count DESC, email ASC
```

**Why it works:**
- `GROUP BY email` groups all rows by email address
- `COUNT(*)` counts how many times each email appears
- `HAVING COUNT(*) > 1` filters out emails that only appear once
- `ORDER BY count DESC, email ASC` sorts by most duplicates first, then alphabetically
