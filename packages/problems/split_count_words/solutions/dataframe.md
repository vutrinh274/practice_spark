## DataFrame API Solution

```python
# F (pyspark.sql.functions) and Window are pre-imported

stop_words = ["the", "and", "for", "this", "was", "very", "are", "with", "that"]

result = (
    df
    .select(F.explode(F.split(F.lower(F.col("review_text")), " ")).alias("word"))
    .filter(F.length(F.col("word")) >= 3)
    .filter(~F.col("word").isin(stop_words))
    .groupBy("word")
    .agg(F.count("*").alias("count"))
    .orderBy(F.col("count").desc(), F.col("word").asc())
    .limit(5)
)
```

**Why it works:**
- `F.lower` + `F.split` converts each review into a lowercased array of words.
- `F.explode` turns the array into individual rows — one word per row.
- `.filter(F.length(...) >= 3)` drops short words; `.filter(~col.isin(...))` drops stop words.
- `.groupBy("word").agg(F.count("*"))` counts each word's frequency.
- `.orderBy(count desc, word asc).limit(5)` returns the top 5 with a deterministic tiebreaker.
