## DataFrame API Solution

```python
# F (pyspark.sql.functions) and Window are pre-imported
# orders and customers are available as variables

result = (
    orders
    .filter(F.col("status") == "completed")
    .join(customers, on="customer_id")
    .select("order_id", "name", "city", "amount")
    .orderBy("order_id")
)
```

**Why it works:**
- Filter before joining for better performance — reduces rows before the join
- `.join(customers, on="customer_id")` performs an inner join by default
- `.select(...)` picks only the required columns
