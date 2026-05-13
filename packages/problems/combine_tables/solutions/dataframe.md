## DataFrame API Solution

```python
# F (pyspark.sql.functions) and Window are pre-imported
# orders_2023 and orders_2024 are available as variables

result = (
    orders_2023
    .unionByName(orders_2024)
    .orderBy("order_id")
)
```

**Why it works:**
- `.unionByName()` stacks rows matching columns by name, not position — safer than `.union()`
- `.orderBy("order_id")` sorts the combined result
