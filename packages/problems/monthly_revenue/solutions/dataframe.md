## DataFrame API Solution

```python
# F (pyspark.sql.functions) and Window are pre-imported

result = (
    df
    .withColumn("month", F.date_format(F.col("order_date"), "yyyy-MM"))
    .groupBy("month")
    .agg(
        F.sum("amount").alias("total_revenue"),
        F.count("*").alias("num_orders")
    )
    .orderBy("month")
)
```

**Why it works:**
- `F.date_format(...)` creates a `yyyy-MM` string column
- `.groupBy("month")` groups all orders in the same month
- `.agg(...)` computes both metrics in one step
