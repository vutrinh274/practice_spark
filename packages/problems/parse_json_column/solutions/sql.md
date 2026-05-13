## SQL Solution

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

**Why it works:**
- `GET_JSON_OBJECT(col, '$.key')` extracts a single value from a JSON string using JSONPath syntax
- All extracted values are strings by default; `CAST(... AS INT)` converts `duration` to the correct type
- No schema definition is needed in SQL — each field is extracted individually
