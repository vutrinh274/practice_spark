from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pathlib import Path

spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()
CONTAINER_BASE = "/problems/column_arithmetic"

df = spark.read.option("header", True).option("inferSchema", True).csv(f"{CONTAINER_BASE}/fixture.csv")

discounted = F.round(F.col("price") * (1 - F.col("discount_pct") / 100.0), 2)

result = (
    df
    .withColumn("discounted_price", discounted)
    .withColumn("total_revenue", F.round(discounted * F.col("quantity"), 2))
    .select("product_id", "product_name", "discounted_price", "total_revenue")
    .orderBy(F.desc("total_revenue"))
)

result.toPandas().to_csv(str(Path(__file__).parent / "expected.csv"), index=False)
print("expected.csv written.")
