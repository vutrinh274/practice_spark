## DataFrame API Solution

```python
# F (pyspark.sql.functions) and Window are pre-imported

w = Window.orderBy("sale_date").rowsBetween(-6, 0)

result = (
    df
    .withColumn("rolling_avg_7d", F.round(F.avg("amount").over(w), 2))
    .select("sale_date", "amount", "rolling_avg_7d")
    .orderBy("sale_date")
)
```

**Why it works:**
- `.rowsBetween(-6, 0)` is the Python equivalent of `ROWS BETWEEN 6 PRECEDING AND CURRENT ROW`
- `F.avg("amount").over(w)` computes the average over the sliding 7-row frame
- `F.round(..., 2)` rounds the result to 2 decimal places
