## DataFrame API Solution

```python
# F (pyspark.sql.functions) and Window are pre-imported
# products and sales are available as variables

window = Window.partitionBy("category").orderBy(F.desc("total_quantity"))

result = (
    products
    .join(sales, on="product_id")
    .groupBy("category", "product_name")
    .agg(F.sum("quantity").alias("total_quantity"))
    .withColumn("rank", F.rank().over(window))
    .filter(F.col("rank") == 1)
    .select("category", "product_name", "total_quantity")
    .orderBy("category")
)
```

**Why it works:**
- Join → aggregate total quantity per product per category
- `F.rank().over(window)` ranks within each category by quantity
- Filter rank == 1 to get the top product
