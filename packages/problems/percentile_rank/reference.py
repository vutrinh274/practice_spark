from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window
from pathlib import Path

spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()
BASE = "/problems/percentile_rank"

df = spark.read.option("header", True).option("inferSchema", True).csv(f"{BASE}/fixture.csv")

w = Window.partitionBy("region").orderBy(F.col("total_sales").desc())

result = (
    df
    .withColumn("pct_rank", F.round(F.percent_rank().over(w), 2))
    .withColumn("quartile", F.ntile(4).over(w))
    .select("rep_id", "name", "region", "total_sales", "pct_rank", "quartile")
    .orderBy("region", F.col("total_sales").desc())
)

result.toPandas().to_csv(str(Path(__file__).parent / "expected.csv"), index=False)
print("expected.csv written.")
