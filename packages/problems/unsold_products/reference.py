from pyspark.sql import SparkSession
from pathlib import Path

spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()
BASE = "/problems/unsold_products"

products = spark.read.option("header", True).option("inferSchema", True).csv(f"{BASE}/products.csv")
sales = spark.read.option("header", True).option("inferSchema", True).csv(f"{BASE}/sales.csv")

result = (
    products
    .join(sales, on="product_id", how="left_anti")
    .select("product_id", "product_name", "category", "price")
    .orderBy("product_id")
)

result.toPandas().to_csv(str(Path(__file__).parent / "expected.csv"), index=False)
print("expected.csv written.")
