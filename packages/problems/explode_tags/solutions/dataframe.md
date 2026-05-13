## DataFrame API Solution

```python
# F (pyspark.sql.functions) and Window are pre-imported

result = (
    df
    .withColumn("tag", F.explode(F.split(F.col("tags"), ",")))
    .select("product_id", "product_name", "tag")
    .orderBy("product_id", "tag")
)
```

**Why it works:**
- `F.split(F.col("tags"), ",")` produces an `ArrayType(StringType)` column
- `F.explode(...)` turns each array element into a separate row, dropping the original array column
- `.select(...)` keeps only the required columns in the correct order
- `.orderBy("product_id", "tag")` produces a deterministic ordering
