## DataFrame API Solution

```python
# F (pyspark.sql.functions) and Window are pre-imported

w = Window.partitionBy("customer_id").orderBy("purchase_date")

result = (
    df
    .withColumn("next_purchase_date", F.lead("purchase_date", 1).over(w))
    .select("purchase_id", "customer_id", "purchase_date", "next_purchase_date")
    .orderBy("customer_id", "purchase_date")
)
```

**Why it works:**
- `Window.partitionBy("customer_id").orderBy("purchase_date")` defines the per-customer chronological window
- `F.lead("purchase_date", 1).over(w)` fetches the next row's purchase date
- The last purchase per customer returns NULL automatically
