## DataFrame API Solution

```python
# F (pyspark.sql.functions) and Window are pre-imported

result = (
    df
    .filter(F.array_contains(F.split(F.col("interests"), ","), "Technology"))
    .select("user_id", "name")
    .orderBy("user_id")
)
```

**Why it works:**
- `F.split(F.col("interests"), ",")` produces an `ArrayType(StringType)` column
- `F.array_contains(array_col, value)` returns a boolean column — `True` when the value is present
- `.filter(...)` keeps only matching rows
- `.select("user_id", "name")` drops the `interests` column from the output
