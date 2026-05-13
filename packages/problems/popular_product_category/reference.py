from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window
from pathlib import Path

spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()
BASE = "/problems/popular_product_category"

products = spark.read.option("header", True).option("inferSchema", True).csv(f"{BASE}/products.csv")
sales = spark.read.option("header", True).option("inferSchema", True).csv(f"{BASE}/sales.csv")

window = Window.partitionBy("category").orderBy(F.desc("total_quantity"))

result = (
    products
    .join(sales, on="product_id")
    .groupBy("category", "product_name")
    .agg(F.sum("quantity").alias("total_quantity"))
    .withColumn("rank", F.rank().over(window))
    .filter(F.col("rank") == 1)
    .select("category", "product_name", "total_quantity")
    .orderBy("category")
)

result.toPandas().to_csv(str(Path(__file__).parent / "expected.csv"), index=False)
print("expected.csv written.")
