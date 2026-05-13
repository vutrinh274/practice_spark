## DataFrame API Solution

```python
# F (pyspark.sql.functions) and Window are pre-imported

window = (
    Window
    .partitionBy("customer_id")
    .orderBy("order_date")
    .rowsBetween(Window.unboundedPreceding, Window.currentRow)
)

result = df \
    .withColumn("running_total", F.sum("amount").over(window)) \
    .select("customer_id", "order_date", "amount", "running_total") \
    .orderBy("customer_id", "order_date")
```

**Why it works:**
- `Window.partitionBy("customer_id")` resets the sum per customer
- `.orderBy("order_date")` accumulates chronologically
- `.rowsBetween(Window.unboundedPreceding, Window.currentRow)` includes all rows from the partition start to current
