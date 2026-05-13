## DataFrame API Solution

```python
# F (pyspark.sql.functions) and Window are pre-imported

w = Window.partitionBy("category").orderBy("year")

result = (
    df
    .withColumn("prev_revenue", F.lag("revenue", 1).over(w))
    .withColumn(
        "yoy_growth_pct",
        F.round((F.col("revenue") - F.col("prev_revenue")) / F.col("prev_revenue") * 100, 2)
    )
    .select("category", "year", "revenue", "yoy_growth_pct")
    .orderBy("category", "year")
)
```

**Why it works:**
- `F.lag("revenue", 1).over(w)` retrieves the previous year's revenue per category
- The growth formula is computed column by column; NULL divided by anything remains NULL
- `F.round(..., 2)` rounds the result
