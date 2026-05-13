from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pathlib import Path

spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()
CONTAINER_BASE = "/problems/filter_and_count"

df = spark.read.option("header", True).option("inferSchema", True).csv(f"{CONTAINER_BASE}/fixture.csv")

result = (
    df
    .filter(F.col("country") == "USA")
    .groupBy("country")
    .agg(
        F.countDistinct("customer_id").alias("distinct_customers"),
        F.sum("amount").alias("total_revenue")
    )
)

result.toPandas().to_csv(str(Path(__file__).parent / "expected.csv"), index=False)
print("expected.csv written.")
