## DataFrame API Solution

```python
# F (pyspark.sql.functions) and Window are pre-imported

discounted = F.round(F.col("price") * (1 - F.col("discount_pct") / 100.0), 2)

result = (
    df
    .withColumn("discounted_price", discounted)
    .withColumn("total_revenue", F.round(discounted * F.col("quantity"), 2))
    .select("product_id", "product_name", "discounted_price", "total_revenue")
    .orderBy(F.desc("total_revenue"))
)
```

**Why it works:**
- Define `discounted` as a reusable column expression
- `.withColumn()` adds derived columns one at a time
- `F.round(..., 2)` rounds to 2 decimal places
