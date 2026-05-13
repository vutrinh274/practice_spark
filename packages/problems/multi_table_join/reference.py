from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pathlib import Path

spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()

CONTAINER_BASE = "/problems/multi_table_join"

orders = spark.read.option("header", True).option("inferSchema", True).csv(f"{CONTAINER_BASE}/orders.csv")
customers = spark.read.option("header", True).option("inferSchema", True).csv(f"{CONTAINER_BASE}/customers.csv")
products = spark.read.option("header", True).option("inferSchema", True).csv(f"{CONTAINER_BASE}/products.csv")

result = (
    orders
    .join(customers, on="customer_id")
    .join(products, on="product_id")
    .withColumn("revenue", F.col("quantity") * F.col("price"))
    .groupBy("customer_id", "name", "city")
    .agg(F.sum("revenue").alias("total_revenue"))
    .orderBy(F.desc("total_revenue"))
)

result.toPandas().to_csv(str(Path(__file__).parent / "expected.csv"), index=False)
print("expected.csv written.")
