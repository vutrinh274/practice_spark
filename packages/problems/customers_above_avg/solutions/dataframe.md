## DataFrame API Solution

```python
# F (pyspark.sql.functions) and Window are pre-imported

totals = (
    df
    .groupBy("customer_id")
    .agg(F.sum("amount").alias("total_spend"))
)

avg_spend = totals.agg(F.avg("total_spend")).collect()[0][0]

result = (
    totals
    .filter(F.col("total_spend") > avg_spend)
    .orderBy(F.col("total_spend").desc())
)
```

**Why it works:**
- First aggregation computes per-customer totals
- `.collect()[0][0]` pulls the single average value to the driver
- The filter then compares each customer's total against that scalar
