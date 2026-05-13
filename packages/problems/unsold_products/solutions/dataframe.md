## DataFrame API Solution

```python
# F (pyspark.sql.functions) and Window are pre-imported
# products and sales are available as variables

result = (
    products
    .join(sales, on="product_id", how="left_anti")
    .select("product_id", "product_name", "category", "price")
    .orderBy("product_id")
)
```

**Why it works:**
- `how="left_anti"` is Spark's built-in anti-join — returns only rows from `products` with no match in `sales`
- Cleaner than LEFT JOIN + IS NULL filter
