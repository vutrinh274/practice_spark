from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pathlib import Path

spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()
BASE = "/problems/first_last_event"

df = spark.read.option("header", True).option("inferSchema", True).csv(f"{BASE}/fixture.csv")

result = (
    df
    .groupBy("user_id")
    .agg(
        F.min("event_date").alias("first_event"),
        F.max("event_date").alias("last_event"),
        F.count("*").alias("total_events")
    )
    .orderBy("user_id")
)

result.toPandas().to_csv(str(Path(__file__).parent / "expected.csv"), index=False)
print("expected.csv written.")
