## DataFrame API Solution

```python
# F (pyspark.sql.functions) and Window are pre-imported

result = (
    df
    .withColumn("tag", F.explode(F.split(F.col("tags"), ",")))
    .groupBy("product_id", "product_name")
    .agg(F.count("tag").alias("tag_count"))
    .orderBy(F.col("tag_count").desc(), F.col("product_id").asc())
)
```

**Why it works:**
- `F.split` and `F.explode` expand each comma-separated tag string into individual rows.
- After grouping, `F.count("tag")` tallies the tags per product.
- Dual sort (`tag_count DESC`, `product_id ASC`) ensures a deterministic order.
