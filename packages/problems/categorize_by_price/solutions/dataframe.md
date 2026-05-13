## DataFrame API Solution

```python
# F (pyspark.sql.functions) and Window are pre-imported

result = (
    df
    .withColumn("price_tier",
        F.when(F.col("price") < 50, "Budget")
         .when(F.col("price") < 500, "Mid-range")
         .otherwise("Premium")
    )
    .select("product_id", "product_name", "price", "price_tier")
    .orderBy("price")
)
```

**Why it works:**
- `F.when(...).when(...).otherwise(...)` chains conditions like CASE WHEN
- Conditions are evaluated in order — first match wins
- `.otherwise("Premium")` is the ELSE clause
