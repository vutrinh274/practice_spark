# Solution: DataFrame API

```python
# F (pyspark.sql.functions) and Window are pre-imported

order_stats = (
    orders
    .groupBy("customer_id")
    .agg(
        F.count("*").alias("total_orders"),
        F.round(F.avg("amount"), 2).alias("avg_order_value"),
    )
)

rating_stats = (
    ratings
    .groupBy("customer_id")
    .agg(F.round(F.avg("score"), 2).alias("avg_rating"))
)

result = (
    order_stats
    .join(rating_stats, on="customer_id")
    .withColumn(
        "loyalty_score",
        F.round(
            F.col("total_orders") * 0.3
            + F.col("avg_order_value") * 0.5
            + F.col("avg_rating") * 0.2,
            2,
        )
    )
    .select("customer_id", "total_orders", "avg_order_value", "avg_rating", "loyalty_score")
    .orderBy(F.col("loyalty_score").desc())
)

result.show()
```

## Explanation

- Each table is aggregated independently before the join, keeping the computation efficient.
- The loyalty formula multiplies each metric by its weight, sums them, and rounds to two decimal places.
- `orderBy(F.col("loyalty_score").desc())` ranks from the most loyal customer downward.
