## DataFrame API Solution

```python
# F (pyspark.sql.functions) and Window are pre-imported

result = (
    df
    .groupBy("sale_date")
    .agg(
        F.sum("amount").alias("total_amount"),
        F.count("*").alias("num_transactions")
    )
    .orderBy("sale_date")
)
```

**Why it works:**
- `.groupBy("sale_date")` groups all transactions by day
- `F.sum("amount")` totals daily sales
- `F.count("*")` counts transactions per day
