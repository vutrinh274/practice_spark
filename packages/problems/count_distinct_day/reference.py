from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pathlib import Path

spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()
BASE = "/problems/count_distinct_day"

df = spark.read.option("header", True).option("inferSchema", True).csv(f"{BASE}/fixture.csv")

result = (
    df
    .groupBy("event_date")
    .agg(
        F.countDistinct("user_id").alias("distinct_users"),
        F.count("*").alias("total_events")
    )
    .orderBy("event_date")
)

result.toPandas().to_csv(str(Path(__file__).parent / "expected.csv"), index=False)
print("expected.csv written.")
