## DataFrame API Solution

```python
# F (pyspark.sql.functions) and Window are pre-imported

result = (
    df
    .groupBy("product_id", "product_name")
    .agg(F.array_join(F.array_sort(F.collect_list("tag")), ",").alias("tags"))
    .orderBy("product_id")
)
```

**Why it works:**
- `F.collect_list("tag")` aggregates tags into an array
- `F.array_sort(...)` ensures consistent ordering
- `F.array_join(..., ",")` converts to a string for reliable comparison
