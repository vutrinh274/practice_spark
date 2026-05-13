## DataFrame API Solution

```python
# F (pyspark.sql.functions) and Window are pre-imported
result = df \
    .groupBy("customer_id") \
    .agg(F.sum("amount").alias("total_amount"))
```

**Why it works:**
- `.groupBy("customer_id")` partitions the DataFrame by `customer_id`
- `.agg(F.sum("amount").alias("total_amount"))` computes the sum per group and names the output column
- `F.sum` is from `pyspark.sql.functions` — always use the functions module for aggregate operations
