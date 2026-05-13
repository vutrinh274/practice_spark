**SQL approach:** Use `GET_JSON_OBJECT(address, '$.street')`, `GET_JSON_OBJECT(address, '$.city')`, and `GET_JSON_OBJECT(address, '$.zip')` to extract each field.

**DataFrame approach:**
1. Define a `StructType` schema: `street`, `city`, `zip` (all StringType).
2. Use `F.from_json(F.col("address"), schema)` to parse the JSON column into a struct named `addr`.
3. In `.select(...)`, reference the sub-fields as `F.col("addr.street")`, `F.col("addr.city")`, `F.col("addr.zip")`.
4. Preserve `order_id`, `customer_name`, and `items_count` from the original row.
