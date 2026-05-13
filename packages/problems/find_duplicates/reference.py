from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pathlib import Path

spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()

CONTAINER_BASE = "/problems/find_duplicates"

users = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(f"{CONTAINER_BASE}/fixture.csv")
)

result = (
    users
    .groupBy("email")
    .agg(F.count("*").alias("count"))
    .filter(F.col("count") > 1)
    .orderBy(F.desc("count"), "email")
)

result.toPandas().to_csv(str(Path(__file__).parent / "expected.csv"), index=False)
print("expected.csv written.")
