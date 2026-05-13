from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window
from pathlib import Path

spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()
BASE = "/problems/etl_job_stats"

df = spark.read.option("header", True).option("inferSchema", True).csv(f"{BASE}/fixture.csv")

agg_df = (
    df
    .withColumn(
        "duration_seconds",
        F.unix_timestamp(F.col("end_time")) - F.unix_timestamp(F.col("start_time"))
    )
    .groupBy("pipeline")
    .agg(
        F.count("job_id").alias("total_runs"),
        F.round(
            F.sum(F.when(F.col("status") == "success", 1).otherwise(0)) * 100.0 / F.count("job_id"),
            2
        ).alias("success_rate"),
        F.round(F.avg("duration_seconds"), 2).alias("avg_duration_seconds"),
        F.round(F.avg("rows_processed"), 2).alias("avg_rows_processed"),
    )
)

w = Window.orderBy(F.col("success_rate").desc())

result = (
    agg_df
    .withColumn("rank", F.dense_rank().over(w))
    .select("pipeline", "total_runs", "success_rate", "avg_duration_seconds", "avg_rows_processed", "rank")
    .orderBy("rank")
)

result.toPandas().to_csv(str(Path(__file__).parent / "expected.csv"), index=False)
print("expected.csv written.")
