## DataFrame API Solution

```python
# F (pyspark.sql.functions) and Window are pre-imported

laptop_buyers = df.filter(F.col("product") == "Laptop").select("customer_id")
phone_buyers = df.filter(F.col("product") == "Phone").select("customer_id")

result = laptop_buyers.intersect(phone_buyers).orderBy("customer_id")
```

**Why it works:**
- Filter each product separately into its own DataFrame
- `.intersect()` returns only `customer_id` values present in both
