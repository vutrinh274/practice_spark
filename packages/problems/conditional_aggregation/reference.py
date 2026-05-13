from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pathlib import Path

spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()
BASE = "/problems/conditional_aggregation"
df = spark.read.option("header", True).option("inferSchema", True).csv(f"{BASE}/fixture.csv")

result = (
    df.groupBy("customer_id").agg(
        F.sum(F.when(F.col("status") == "completed", F.col("amount")).otherwise(0)).alias("completed_revenue"),
        F.sum(F.when(F.col("status") == "cancelled", F.col("amount")).otherwise(0)).alias("cancelled_revenue"),
        F.count("*").alias("total_orders")
    ).orderBy("customer_id")
)
result.toPandas().to_csv(str(Path(__file__).parent / "expected.csv"), index=False)
print("expected.csv written.")
