## DataFrame API Solution

```python
# F (pyspark.sql.functions) and Window are pre-imported
# customers and orders are available as variables

result = (
    customers
    .join(orders, on="customer_id", how="left")
    .filter(F.col("order_id").isNull())
    .select("customer_id", "name", "city", "signup_date")
    .orderBy("customer_id")
)
```

**Why it works:**
- `how="left"` keeps all customers even without matching orders
- `.filter(F.col("order_id").isNull())` — the anti-join filter
- Spark also supports `how="left_anti"` which does this in one step: `.join(orders, on="customer_id", how="left_anti")`
