## DataFrame API Solution

```python
# F (pyspark.sql.functions) and Window are pre-imported

result = (
    df
    .withColumn("original_phone", F.col("phone"))
    .withColumn("digits", F.regexp_replace(F.col("phone"), "[^0-9]", ""))
    .withColumn(
        "standardized_phone",
        F.concat(
            F.substring(F.col("digits"), 1, 3),
            F.lit("-"),
            F.substring(F.col("digits"), 4, 3),
            F.lit("-"),
            F.substring(F.col("digits"), 7, 4),
        )
    )
    .select("contact_id", "name", "original_phone", "standardized_phone")
    .orderBy("contact_id")
)
```

**Why it works:**
- `F.regexp_replace(col, "[^0-9]", "")` removes all non-digit characters, leaving a clean 10-digit string.
- `F.substring(col, 1, 3)` / `(col, 4, 3)` / `(col, 7, 4)` slices the three groups of digits (Spark uses 1-based indexing).
- `F.lit("-")` inserts the literal dash separator.
- `F.concat(...)` assembles everything into `XXX-XXX-XXXX`.
