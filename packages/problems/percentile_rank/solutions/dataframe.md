## DataFrame API Solution

```python
# F (pyspark.sql.functions) and Window are pre-imported

w = Window.partitionBy("region").orderBy(F.col("total_sales").desc())

result = (
    df
    .withColumn("pct_rank", F.round(F.percent_rank().over(w), 2))
    .withColumn("quartile", F.ntile(4).over(w))
    .select("rep_id", "name", "region", "total_sales", "pct_rank", "quartile")
    .orderBy("region", F.col("total_sales").desc())
)
```

**Why it works:**
- `F.percent_rank()` and `F.ntile(4)` are applied over the same descending window
- Both functions require an ordered window specification
- `F.round(..., 2)` rounds the percent rank output
