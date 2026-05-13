## DataFrame API Solution

```python
# F (pyspark.sql.functions) and Window are pre-imported

stats = df.agg(
    F.percentile_approx("amount", 0.25).alias("q1"),
    F.percentile_approx("amount", 0.75).alias("q3")
).collect()[0]

q1, q3 = stats["q1"], stats["q3"]
iqr = q3 - q1
lower = q1 - 1.5 * iqr
upper = q3 + 1.5 * iqr

result = (
    df
    .filter((F.col("amount") >= lower) & (F.col("amount") <= upper))
    .orderBy("transaction_id")
)
```

**Why it works:**
- `F.percentile_approx` computes approximate quantiles efficiently on large datasets
- The bounds are computed on the driver and used as scalar filter values
- The filter retains only non-outlier rows
