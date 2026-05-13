## DataFrame API Solution

```python
# F (pyspark.sql.functions) and Window are pre-imported

stage_order = {"view": 1, "cart": 2, "checkout": 3, "purchase": 4}

counts = (
    user_events
    .groupBy(F.col("event_type").alias("stage"))
    .agg(F.countDistinct("user_id").alias("users_reached"))
)

result = (
    counts
    .withColumn("stage_order",
        F.when(F.col("stage") == "view", 1)
         .when(F.col("stage") == "cart", 2)
         .when(F.col("stage") == "checkout", 3)
         .when(F.col("stage") == "purchase", 4)
    )
    .select("stage", "stage_order", "users_reached")
    .orderBy("stage_order")
)
```

**Why it works:**
- `F.countDistinct("user_id")` counts unique users per event type
- `F.when(...).when(...)` assigns stage_order without needing spark.createDataFrame
- `.orderBy("stage_order")` presents funnel from top to bottom
