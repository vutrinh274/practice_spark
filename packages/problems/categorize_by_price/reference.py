from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pathlib import Path

spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()
CONTAINER_BASE = "/problems/categorize_by_price"

df = spark.read.option("header", True).option("inferSchema", True).csv(f"{CONTAINER_BASE}/fixture.csv")

result = (
    df
    .withColumn("price_tier",
        F.when(F.col("price") < 50, "Budget")
         .when(F.col("price") < 500, "Mid-range")
         .otherwise("Premium")
    )
    .select("product_id", "product_name", "price", "price_tier")
    .orderBy("price")
)

result.toPandas().to_csv(str(Path(__file__).parent / "expected.csv"), index=False)
print("expected.csv written.")
