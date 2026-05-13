```sql
SELECT user_id, name
FROM user_interests
WHERE ARRAY_CONTAINS(SPLIT(interests, ','), 'Technology')
ORDER BY user_id
```
