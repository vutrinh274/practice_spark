## DataFrame API Solution

```python
# F (pyspark.sql.functions) and Window are pre-imported

w = Window.partitionBy("stock").orderBy("price_date")

result = (
    df
    .withColumn("price_change", F.col("close_price") - F.lag("close_price", 1).over(w))
    .select("stock", "price_date", "close_price", "price_change")
    .orderBy("stock", "price_date")
)
```

**Why it works:**
- `Window.partitionBy("stock").orderBy("price_date")` defines the window spec
- `F.lag("close_price", 1).over(w)` retrieves the previous row's close price within each stock's window
- Subtracting yields the daily change; the first row per stock gets NULL
