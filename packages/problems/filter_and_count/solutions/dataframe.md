## DataFrame API Solution

```python
# F (pyspark.sql.functions) and Window are pre-imported

result = (
    df
    .filter(F.col("country") == "USA")
    .groupBy("country")
    .agg(
        F.countDistinct("customer_id").alias("distinct_customers"),
        F.sum("amount").alias("total_revenue")
    )
)
```

**Why it works:**
- `.filter(...)` narrows to USA orders only
- `F.countDistinct("customer_id")` counts unique customers
- `F.sum("amount")` totals revenue
