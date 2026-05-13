## DataFrame API Solution

```python
# F (pyspark.sql.functions) and Window are pre-imported

result = (
    df
    .withColumn(
        "masked_email",
        F.concat(
            F.substring(F.col("email"), 1, 3),
            F.lit("***@"),
            F.regexp_extract(F.col("email"), "@(.+)$", 1),
        )
    )
    .withColumn(
        "masked_phone",
        F.concat(
            F.lit("***-***-"),
            F.substring(F.col("phone"), F.length(F.col("phone")) - 3, 4),
        )
    )
    .select("customer_id", "name", "masked_email", "masked_phone")
    .orderBy("customer_id")
)
```

**Why it works:**
- `F.substring(col, 1, 3)` extracts the first 3 characters of the email local part.
- `F.lit("***@")` inserts the mask literal.
- `F.regexp_extract(col, "@(.+)$", 1)` extracts the domain after `@`.
- `F.length(col) - 3` positions 4 chars from the end — the last 4 digits of the phone.
- `F.lit("***-***-")` prepends the mask for the phone.
