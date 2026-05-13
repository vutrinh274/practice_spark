from pyspark.sql import SparkSession
from pathlib import Path

spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()
CONTAINER_BASE = "/problems/combine_tables"

orders_2023 = spark.read.option("header", True).option("inferSchema", True).csv(f"{CONTAINER_BASE}/fixture_2023.csv")
orders_2024 = spark.read.option("header", True).option("inferSchema", True).csv(f"{CONTAINER_BASE}/fixture_2024.csv")

result = orders_2023.unionByName(orders_2024).orderBy("order_id")

result.toPandas().to_csv(str(Path(__file__).parent / "expected.csv"), index=False)
print("expected.csv written.")
