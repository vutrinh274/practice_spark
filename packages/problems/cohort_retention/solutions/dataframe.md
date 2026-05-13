## DataFrame API Solution

```python
# F (pyspark.sql.functions) and Window are pre-imported

result = (
    df
    .withColumn("cohort_month", F.date_format(F.col("signup_date"), "yyyy-MM"))
    .withColumn(
        "months_since_signup",
        F.months_between(
            F.to_date(F.col("activity_date")),
            F.to_date(F.col("signup_date"))
        ).cast("int")
    )
    .filter((F.col("months_since_signup") >= 0) & (F.col("months_since_signup") <= 3))
    .groupBy("cohort_month", "months_since_signup")
    .agg(F.countDistinct("user_id").alias("active_users"))
    .orderBy("cohort_month", "months_since_signup")
)
```

**Why it works:**
- `F.date_format` extracts the cohort month as a `yyyy-MM` string
- `F.months_between` computes fractional months between two dates; `.cast("int")` truncates to whole months
- `F.to_date` ensures date arithmetic is performed on date types, not strings
- `F.countDistinct("user_id")` counts each user only once within a cohort/month bucket
