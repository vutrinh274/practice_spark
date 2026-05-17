from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window
from pathlib import Path

spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()
BASE = "/problems/scd_type2_modelling"

df = spark.read.option("header", True).option("inferSchema", True).csv(f"{BASE}/fixture.csv")

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

result.toPandas().to_csv(str(Path(__file__).parent / "expected.csv"), index=False)
print("expected.csv written.")
