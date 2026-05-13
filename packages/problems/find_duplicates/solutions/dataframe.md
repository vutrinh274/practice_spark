## DataFrame API Solution

```python
# F (pyspark.sql.functions) and Window are pre-imported

result = df \
    .groupBy("email") \
    .agg(F.count("*").alias("count")) \
    .filter(F.col("count") > 1) \
    .orderBy(F.desc("count"), "email")
```

**Why it works:**
- `.groupBy("email")` groups by email address
- `.agg(F.count("*").alias("count"))` counts occurrences per group
- `.filter(F.col("count") > 1)` keeps only duplicates
- `.orderBy(F.desc("count"), "email")` sorts as required
