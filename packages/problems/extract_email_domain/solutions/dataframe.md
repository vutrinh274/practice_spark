## DataFrame API Solution

```python
# F (pyspark.sql.functions) and Window are pre-imported

result = (
    df
    .withColumn("domain", F.regexp_extract(F.col("email"), "@(.+)$", 1))
    .select("user_id", "name", "email", "domain")
    .orderBy("user_id")
)
```

**Why it works:**
- `F.regexp_extract(col, pattern, groupIndex)` extracts the matched group from the regex.
- Pattern `@(.+)$` captures everything after the `@` symbol.
- `groupIndex=1` returns the first (and only) capture group — the domain.
