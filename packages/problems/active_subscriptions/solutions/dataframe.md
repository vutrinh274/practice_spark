## DataFrame API Solution

```python
# F (pyspark.sql.functions) and Window are pre-imported

target_date = "2024-06-15"

result = (
    df
    .filter(
        (F.col("start_date") <= target_date) &
        (F.col("end_date") >= target_date)
    )
    .select("sub_id", "customer_id", "plan", "start_date", "end_date")
    .orderBy("sub_id")
)
```

**Why it works:**
- String comparison on `yyyy-MM-dd` format is equivalent to date comparison
- `&` combines both filter conditions (use parentheses around each condition)
- `.select(...)` returns only the required columns in the specified order
