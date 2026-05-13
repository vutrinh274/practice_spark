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
