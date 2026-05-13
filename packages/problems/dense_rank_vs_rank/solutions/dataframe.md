## DataFrame API Solution

```python
# F (pyspark.sql.functions) and Window are pre-imported

w = Window.orderBy(F.col("score").desc())

result = (
    df
    .withColumn("rank", F.rank().over(w))
    .withColumn("dense_rank", F.dense_rank().over(w))
    .select("student_id", "name", "score", "rank", "dense_rank")
    .orderBy(F.col("score").desc(), "student_id")
)
```

**Why it works:**
- `Window.orderBy(F.col("score").desc())` ranks all rows globally by score
- `F.rank()` and `F.dense_rank()` are applied over the same window
- The final `orderBy` ensures a deterministic row order when scores are tied
