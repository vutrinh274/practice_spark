from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window
from pathlib import Path

spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()
BASE = "/problems/yoy_growth"

df = spark.read.option("header", True).option("inferSchema", True).csv(f"{BASE}/fixture.csv")

w = Window.partitionBy("category").orderBy("year")

result = (
    df
    .withColumn("prev_revenue", F.lag("revenue", 1).over(w))
    .withColumn(
        "yoy_growth_pct",
        F.round((F.col("revenue") - F.col("prev_revenue")) / F.col("prev_revenue") * 100, 2)
    )
    .select("category", "year", "revenue", "yoy_growth_pct")
    .orderBy("category", "year")
)

result.toPandas().to_csv(str(Path(__file__).parent / "expected.csv"), index=False)
print("expected.csv written.")
