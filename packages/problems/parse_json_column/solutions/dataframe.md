## DataFrame API Solution

```python
# F (pyspark.sql.functions) and Window are pre-imported

json_schema = "struct<page:string,duration:string,referrer:string>"

result = (
    df
    .withColumn("parsed", F.from_json(F.col("properties"), json_schema))
    .select(
        "event_id", "user_id", "event_type",
        F.col("parsed.page").alias("page"),
        F.col("parsed.duration").alias("duration"),
        F.col("parsed.referrer").alias("referrer"),
    )
    .orderBy("event_id")
)
```

**Why it works:**
- `json_schema` is a DDL string defining the JSON structure — no imports needed
- `F.from_json(col, schema)` parses the JSON string into a struct column
- Dot notation (`parsed.page`) accesses struct fields
