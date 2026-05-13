## DataFrame API Solution

```python
# F (pyspark.sql.functions) and Window are pre-imported

exploded = df.select("category", F.explode(F.split("tags", ",")).alias("tag"))

counts = exploded.groupBy("category", "tag").agg(F.count("*").alias("tag_count"))

w = Window.partitionBy("category").orderBy(F.col("tag_count").desc())

result = (
    counts
    .withColumn("rnk", F.rank().over(w))
    .filter(F.col("rnk") == 1)
    .select("category", "tag", "tag_count")
    .orderBy("category")
)
```

**Why it works:**
- `F.explode(F.split(...))` unpacks the comma-separated tags into individual rows.
- After grouping and counting, a `Window` partitioned by `category` and ordered by `tag_count DESC` lets `F.rank()` assign the same rank to tied values.
- Filtering `rnk == 1` selects only the most common tag(s) per category.
