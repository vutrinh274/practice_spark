# Solution: DataFrame API

```python
# F (pyspark.sql.functions) and Window are pre-imported

w = Window.partitionBy("district").orderBy(F.col("votes").desc())

result = (
    votes
    .groupBy("district", "candidate")
    .agg(F.count("*").alias("votes"))
    .withColumn("rnk", F.rank().over(w))
    .filter(F.col("rnk") == 1)
    .select("district", "candidate", "votes")
    .orderBy("district")
)

result.show()
```

## Explanation

- `groupBy("district", "candidate").agg(count("*"))` tallies each candidate's votes per district.
- `rank().over(w)` ranks candidates within each district by vote count descending. The leading candidate gets rank 1.
- Filtering `rnk == 1` retains only the winner(s) per district.
- `select` and `orderBy` produce the clean final output.
