## DataFrame API Solution

```python
# F (pyspark.sql.functions) and Window are pre-imported

window = Window.partitionBy("department").orderBy(F.desc("salary"))

result = df \
    .withColumn("rank", F.rank().over(window)) \
    .filter(F.col("rank") <= 2) \
    .orderBy("department", "rank")
```

**Why it works:**
- `Window.partitionBy("department").orderBy(F.desc("salary"))` defines a window per department sorted by salary descending
- `F.rank().over(window)` assigns rank 1 to the highest salary in each department
- `.filter(F.col("rank") <= 2)` keeps only top 2 per department
