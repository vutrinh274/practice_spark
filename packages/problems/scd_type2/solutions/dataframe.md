## DataFrame API Solution

```python
# F (pyspark.sql.functions) and Window are pre-imported

w = Window.partitionBy("employee_id").orderBy("effective_date")

result = (
    df
    .withColumn("end_date", F.lead("effective_date").over(w))
    .withColumn("is_current", F.when(F.col("end_date").isNull(), 1).otherwise(0))
    .select(
        "record_id",
        "employee_id",
        "name",
        "department",
        "salary",
        "effective_date",
        "end_date",
        "is_current",
    )
    .orderBy("employee_id", "effective_date")
)
```

**Why it works:**
- `F.lead("effective_date").over(w)` reads the next row's `effective_date` within the employee partition, ordered chronologically
- The last record per employee gets NULL from `F.lead` — there is no following row
- `F.when(F.col("end_date").isNull(), 1).otherwise(0)` converts the NULL into a binary `is_current` flag
- The explicit `.select(...)` ensures column order matches the expected output exactly
