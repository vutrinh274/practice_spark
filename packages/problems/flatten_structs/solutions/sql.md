## SQL Solution

```sql
SELECT
    order_id,
    customer_name,
    GET_JSON_OBJECT(address, '$.street') AS street,
    GET_JSON_OBJECT(address, '$.city') AS city,
    GET_JSON_OBJECT(address, '$.zip') AS zip,
    items_count
FROM orders
ORDER BY order_id
```

**Why it works:**
- `GET_JSON_OBJECT` uses JSONPath (`$.key`) to extract each field from the JSON string
- The original columns (`order_id`, `customer_name`, `items_count`) are passed through unchanged
- All extracted address fields are strings, so no casting is required here
