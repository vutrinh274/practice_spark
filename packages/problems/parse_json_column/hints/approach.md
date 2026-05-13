**SQL approach:** Use `GET_JSON_OBJECT(properties, '$.page')` to extract each key by its JSONPath expression. Cast `duration` to INT since `GET_JSON_OBJECT` always returns a string.

**DataFrame approach:**
1. Define a `StructType` schema matching the JSON keys: `page` (StringType), `duration` (IntegerType), `referrer` (StringType).
2. Apply `F.from_json(F.col("properties"), schema)` to parse the column into a struct.
3. Select individual fields from the struct using dot notation: `F.col("parsed.page")`.
