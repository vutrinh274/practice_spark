from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pathlib import Path

spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()
CONTAINER_BASE = "/problems/daily_sales"

df = spark.read.option("header", True).option("inferSchema", True).csv(f"{CONTAINER_BASE}/fixture.csv")

result = (
    df
    .groupBy("sale_date")
    .agg(
        F.sum("amount").alias("total_amount"),
        F.count("*").alias("num_transactions")
    )
    .orderBy("sale_date")
)

result.toPandas().to_csv(str(Path(__file__).parent / "expected.csv"), index=False)
print("expected.csv written.")
