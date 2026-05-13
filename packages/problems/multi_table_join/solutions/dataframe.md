## DataFrame API Solution

```python
# F (pyspark.sql.functions) and Window are pre-imported
# All tables are available as variables: orders, customers, products

result = (
    orders
    .join(customers, on="customer_id")
    .join(products, on="product_id")
    .withColumn("revenue", F.col("quantity") * F.col("price"))
    .groupBy("customer_id", "name", "city")
    .agg(F.sum("revenue").alias("total_revenue"))
    .orderBy(F.desc("total_revenue"))
)
```

**Why it works:**
- `.join(customers, on="customer_id")` links orders to customer info
- `.join(products, on="product_id")` links to product prices
- `.withColumn("revenue", ...)` computes per-order revenue
- `.groupBy(...).agg(F.sum(...))` aggregates per customer
