from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window
from pathlib import Path

spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()
BASE = "/problems/increasing_yoy_sales"

df = spark.read.option("header", True).option("inferSchema", True).csv(f"{BASE}/fixture.csv")

w = Window.partitionBy("product_id").orderBy("year")

with_lag = df.withColumn("prev_sales", F.lag("total_sales").over(w))

with_growth = with_lag.withColumn(
    "yoy_growth",
    F.col("total_sales") - F.col("prev_sales")
)

qualified = (
    with_growth
    .filter(F.col("prev_sales").isNotNull())
    .groupBy("product_id", "product_name")
    .agg(F.min("yoy_growth").alias("min_growth"))
    .filter(F.col("min_growth") > 0)
    .select("product_id", "product_name")
    .orderBy("product_id")
)

result = qualified

result.toPandas().to_csv(str(Path(__file__).parent / "expected.csv"), index=False)
print("expected.csv written.")
