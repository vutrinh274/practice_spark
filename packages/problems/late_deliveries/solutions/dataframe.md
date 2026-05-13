## DataFrame API Solution

```python
# F (pyspark.sql.functions) and Window are pre-imported

result = (
    df
    .withColumn("actual_days", F.datediff(F.col("delivery_date"), F.col("order_date")))
    .withColumn("days_late", F.col("actual_days") - F.col("promised_days"))
    .filter(F.col("actual_days") > F.col("promised_days"))
    .select("order_id", "customer_id", "promised_days", "actual_days", "days_late")
    .orderBy(F.col("days_late").desc())
)
```

**Why it works:**
- `F.datediff(end, start)` returns the integer number of days — delivery_date minus order_date
- `.withColumn("days_late", ...)` computes the delay in one step
- `.filter(...)` removes on-time and early deliveries
- `.orderBy(F.col("days_late").desc())` sorts from most delayed to least
