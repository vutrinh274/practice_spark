## DataFrame API Solution

```python
# F (pyspark.sql.functions) and Window are pre-imported

w = Window.partitionBy("region").orderBy(F.col("total_spend").desc())

result = (
    df
    .withColumn("rank", F.rank().over(w))
    .filter(F.col("rank") <= 2)
    .select("region", "customer_id", "name", "total_spend", "rank")
    .orderBy("region", "rank")
)
```

**Why it works:**
- `F.rank().over(w)` assigns ranks within each region by descending spend
- `.filter(F.col("rank") <= 2)` keeps only the top 2 per region
- In the DataFrame API, filtering on a window column works directly (unlike SQL where a subquery is needed)
