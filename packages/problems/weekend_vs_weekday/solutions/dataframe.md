## DataFrame API Solution

```python
# F (pyspark.sql.functions) and Window are pre-imported

result = (
    df
    .withColumn(
        "day_type",
        F.when(F.dayofweek(F.col("sale_date")).isin(1, 7), "Weekend").otherwise("Weekday")
    )
    .groupBy("day_type")
    .agg(
        F.sum("amount").alias("total_revenue"),
        F.count("*").alias("num_sales")
    )
    .orderBy("day_type")
)
```

**Why it works:**
- `F.dayofweek(...)` returns 1 (Sunday) through 7 (Saturday)
- `.isin(1, 7)` matches both weekend days in a concise expression
- `F.when(...).otherwise(...)` is the DataFrame equivalent of `CASE WHEN`
- `.groupBy` and `.agg` compute the revenue and count per bucket
