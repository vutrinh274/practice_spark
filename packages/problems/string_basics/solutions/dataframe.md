## DataFrame API Solution

```python
# F (pyspark.sql.functions) and Window are pre-imported

result = (
    df
    .withColumn("full_name", F.initcap(F.concat(F.trim(F.col("first_name")), F.lit(" "), F.trim(F.col("last_name")))))
    .withColumn("email", F.lower(F.trim(F.col("email"))))
    .withColumn("city", F.initcap(F.trim(F.col("city"))))
    .select("customer_id", "full_name", "email", "city")
    .orderBy("customer_id")
)
```

**Why it works:**
- `F.trim()` removes whitespace
- `F.concat()` joins strings; `F.lit(" ")` is a literal space character
- `F.initcap()` applies Title Case
- `F.lower()` lowercases the email
