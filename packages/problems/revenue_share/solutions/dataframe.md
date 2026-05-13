## DataFrame API Solution

```python
# F (pyspark.sql.functions) and Window are pre-imported

totals = (
    df.groupBy("category")
    .agg(F.sum("amount").alias("total_revenue"))
)

grand_total_window = Window.rowsBetween(Window.unboundedPreceding, Window.unboundedFollowing)

result = (
    totals
    .withColumn("revenue_pct",
        F.round(F.col("total_revenue") * 100.0 / F.sum("total_revenue").over(grand_total_window), 2)
    )
    .orderBy(F.desc("revenue_pct"))
)
```

**Why it works:**
- Aggregate per category first
- `Window.rowsBetween(unboundedPreceding, unboundedFollowing)` spans all rows — gives grand total
- Divide to get percentage, round to 2 decimal places
