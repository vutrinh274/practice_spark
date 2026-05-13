## DataFrame API Solution

```python
# F (pyspark.sql.functions) and Window are pre-imported

w = Window.partitionBy("product_id").orderBy("year")

result = (
    df
    .withColumn("prev_sales", F.lag("total_sales").over(w))
    .withColumn("yoy_growth", F.col("total_sales") - F.col("prev_sales"))
    .filter(F.col("prev_sales").isNotNull())
    .groupBy("product_id", "product_name")
    .agg(F.min("yoy_growth").alias("min_growth"))
    .filter(F.col("min_growth") > 0)
    .select("product_id", "product_name")
    .orderBy("product_id")
)
```

**Why it works:**
- `F.lag("total_sales").over(w)` retrieves the prior year's sales for each product; NULL for the first year
- `.filter(F.col("prev_sales").isNotNull())` removes the first-year rows before aggregation
- `F.min("yoy_growth")` finds the worst YoY performance across all years for each product
- `.filter(F.col("min_growth") > 0)` keeps only products where even the smallest YoY change was positive
