```sql
SELECT
    event_id,
    user_id,
    event_type,
    GET_JSON_OBJECT(properties, '$.page') AS page,
    CAST(GET_JSON_OBJECT(properties, '$.duration') AS INT) AS duration,
    GET_JSON_OBJECT(properties, '$.referrer') AS referrer
FROM events
ORDER BY event_id
```
