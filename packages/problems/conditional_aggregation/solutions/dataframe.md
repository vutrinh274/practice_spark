## DataFrame API Solution

```python
# F (pyspark.sql.functions) and Window are pre-imported

result = (
    df
    .groupBy("customer_id")
    .agg(
        F.sum(F.when(F.col("status") == "completed", F.col("amount")).otherwise(0)).alias("completed_revenue"),
        F.sum(F.when(F.col("status") == "cancelled", F.col("amount")).otherwise(0)).alias("cancelled_revenue"),
        F.count("*").alias("total_orders")
    )
    .orderBy("customer_id")
)
```

**Why it works:**
- `F.when(...).otherwise(0)` mirrors CASE WHEN ... ELSE 0
- `F.sum(...)` wraps it to sum only the matching amounts
