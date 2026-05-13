## DataFrame API Solution

```python
# F (pyspark.sql.functions) and Window are pre-imported

result = (
    df
    .orderBy(F.desc("total_sales"))
    .limit(5)
    .select("product_id", "product_name", "category", "total_sales")
)
```

**Why it works:**
- `.orderBy(F.desc("total_sales"))` sorts highest sales first
- `.limit(5)` keeps only the top 5 rows
