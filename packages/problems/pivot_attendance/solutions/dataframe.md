## DataFrame API Solution

```python
# F (pyspark.sql.functions) and Window are pre-imported

result = (
    df
    .groupBy("employee_id")
    .pivot("status", ["Present", "Absent", "Late"])
    .count()
    .orderBy("employee_id")
)
```

**Why it works:**
- `.groupBy("employee_id")` groups rows per employee
- `.pivot("status", [...])` specifies the column whose values become new columns; providing the list explicitly avoids an extra scan to discover values
- `.count()` is the aggregation — counts rows matching each status per employee
