# Query Hint

## SQL Skeleton

```sql
WITH vote_counts AS (
    SELECT
        district,
        candidate,
        COUNT(*) AS votes
    FROM votes
    GROUP BY district, candidate
),
ranked AS (
    SELECT
        district,
        candidate,
        votes,
        RANK() OVER (PARTITION BY district ORDER BY votes DESC) AS rnk
    FROM vote_counts
)
SELECT district, candidate, votes
FROM ranked
WHERE rnk = 1
ORDER BY district
```

## DataFrame Skeleton

```python
w = Window.partitionBy("district").orderBy(F.col("votes").desc())

result = (
    votes.groupBy("district", "candidate")
         .agg(F.count("*").alias("votes"))
         .withColumn("rnk", F.rank().over(w))
         .filter(F.col("rnk") == 1)
         .select("district", "candidate", "votes")
         .orderBy("district")
)
```
