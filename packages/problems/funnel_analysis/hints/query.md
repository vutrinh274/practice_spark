# Query Hint

## SQL Skeleton

```sql
WITH stage_map AS (
    SELECT 'view'     AS stage, 1 AS stage_order UNION ALL
    SELECT 'cart'     AS stage, 2 AS stage_order UNION ALL
    SELECT 'checkout' AS stage, 3 AS stage_order UNION ALL
    SELECT 'purchase' AS stage, 4 AS stage_order
),
counts AS (
    SELECT event_type AS stage, COUNT(DISTINCT user_id) AS users_reached
    FROM user_events
    GROUP BY event_type
)
SELECT c.stage, s.stage_order, c.users_reached
FROM counts c
JOIN stage_map s ON c.stage = s.stage
ORDER BY s.stage_order
```

## DataFrame Skeleton

```python
from pyspark.sql import Row

stage_map = spark.createDataFrame([
    Row(stage="view", stage_order=1),
    Row(stage="cart", stage_order=2),
    Row(stage="checkout", stage_order=3),
    Row(stage="purchase", stage_order=4),
])

counts = (
    df.groupBy(F.col("event_type").alias("stage"))
      .agg(F.countDistinct("user_id").alias("users_reached"))
)

result = (
    counts.join(stage_map, on="stage")
          .select("stage", "stage_order", "users_reached")
          .orderBy("stage_order")
)
```
