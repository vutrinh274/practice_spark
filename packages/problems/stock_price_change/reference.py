from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window
from pathlib import Path

spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()
BASE = "/problems/stock_price_change"

df = spark.read.option("header", True).option("inferSchema", True).csv(f"{BASE}/fixture.csv")

w = Window.partitionBy("stock").orderBy("price_date")

result = (
    df
    .withColumn("price_change", F.col("close_price") - F.lag("close_price", 1).over(w))
    .select("stock", "price_date", "close_price", "price_change")
    .orderBy("stock", "price_date")
)

result.toPandas().to_csv(str(Path(__file__).parent / "expected.csv"), index=False)
print("expected.csv written.")
