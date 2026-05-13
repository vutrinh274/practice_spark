## DataFrame API Solution

```python
# F (pyspark.sql.functions) and Window are pre-imported

json_schema = "struct<street:string,city:string,zip:string>"

result = (
    df
    .withColumn("addr", F.from_json(F.col("address"), json_schema))
    .select(
        "order_id", "customer_name",
        F.col("addr.street").alias("street"),
        F.col("addr.city").alias("city"),
        F.col("addr.zip").alias("zip"),
        "items_count",
    )
    .orderBy("order_id")
)
```

**Why it works:**
- DDL schema string defines the JSON structure without any imports
- `F.from_json` parses the address JSON into a struct column
- Dot notation accesses nested struct fields
