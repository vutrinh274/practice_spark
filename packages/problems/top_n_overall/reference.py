from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pathlib import Path

spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()
CONTAINER_BASE = "/problems/top_n_overall"

df = spark.read.option("header", True).option("inferSchema", True).csv(f"{CONTAINER_BASE}/fixture.csv")

result = (
    df
    .orderBy(F.desc("total_sales"))
    .limit(5)
    .select("product_id", "product_name", "category", "total_sales")
)

result.toPandas().to_csv(str(Path(__file__).parent / "expected.csv"), index=False)
print("expected.csv written.")
