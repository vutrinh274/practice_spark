## DataFrame API Solution

```python
# F (pyspark.sql.functions) and Window are pre-imported

w = Window.partitionBy("player_name").orderBy("season")

changes = (
    df
    .withColumn("prev_class", F.lag("scoring_class").over(w))
    .withColumn("prev_active", F.lag("is_active").over(w))
    .withColumn(
        "is_change",
        F.when(
            F.col("prev_class").isNull()
            | (F.col("scoring_class") != F.col("prev_class"))
            | (F.col("is_active") != F.col("prev_active")),
            1,
        ).otherwise(0),
    )
    .withColumn("streak_id", F.sum("is_change").over(w))
    .withColumn(
        "current_season",
        F.max("season").over(Window.partitionBy("player_name")),
    )
)

result = (
    changes
    .groupBy(
        "player_name",
        "streak_id",
        "scoring_class",
        "is_active",
        "current_season",
    )
    .agg(
        F.min("season").alias("start_season"),
        F.max("season").alias("end_season"),
    )
    .select(
        "player_name",
        "scoring_class",
        "is_active",
        "current_season",
        "start_season",
        "end_season",
    )
    .orderBy("player_name", "start_season")
)
```

**Why it works:**
- `F.lag("scoring_class")` and `F.lag("is_active")` over `(player_name, season)` give each row its predecessor's attributes within the same player.
- `is_change = 1` whenever either previous attribute is missing (first row) or differs, so it lights up only on transitions.
- A cumulative `F.sum("is_change")` over the same ordered window yields `streak_id`: every row in the same run shares the same id.
- An unordered `F.max("season").over(Window.partitionBy("player_name"))` attaches `current_season` to each row before the aggregation, so it survives the grouping without an extra join.
- Grouping by `(player_name, streak_id, scoring_class, is_active, current_season)` and aggregating `min`/`max` on `season` collapses each run into a single row with its bounds.
- The explicit `.select(...)` pins the column order to match the expected output.
