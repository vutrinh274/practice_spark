## DataFrame API Solution

```python
# F (pyspark.sql.functions) and Window are pre-imported

pivoted = (
    df
    .groupBy("user_id")
    .agg(
        F.max(F.when(F.col("event_type") == "signup", F.col("event_date"))).alias("signup_date"),
        F.max(F.when(F.col("event_type") == "first_purchase", F.col("event_date"))).alias("first_purchase_date"),
    )
)

result = (
    pivoted
    .withColumn("days_to_purchase", F.datediff(F.col("first_purchase_date"), F.col("signup_date")))
    .select("user_id", "signup_date", "first_purchase_date", "days_to_purchase")
    .orderBy("user_id")
)
```

**Why it works:**
- `F.when(...).otherwise(None)` inside `F.max(...)` extracts the date only for the relevant event type
- `F.datediff(end, start)` returns an integer number of days — note the argument order: end date first
- `.select(...)` ensures the output columns are in the required order
