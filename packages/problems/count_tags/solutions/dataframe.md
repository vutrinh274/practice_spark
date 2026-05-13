## DataFrame API Solution

```python
# F (pyspark.sql.functions) and Window are pre-imported

result = (
    df
    .withColumn("tag_count", F.size(F.split(F.col("tags"), ",")))
    .select("product_id", "product_name", "tag_count")
    .orderBy(F.col("tag_count").desc(), F.col("product_id"))
)
```

**Why it works:**
- `F.split(F.col("tags"), ",")` creates an array column from the comma-separated string
- `F.size(...)` returns the length of the array as an integer column
- `.orderBy(F.col("tag_count").desc(), F.col("product_id"))` sorts by count descending, breaking ties by product_id ascending
