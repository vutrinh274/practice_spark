from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window
from pathlib import Path

spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()
BASE = "/problems/revenue_share"
df = spark.read.option("header", True).option("inferSchema", True).csv(f"{BASE}/fixture.csv")

totals = df.groupBy("category").agg(F.sum("amount").alias("total_revenue"))
w = Window.rowsBetween(Window.unboundedPreceding, Window.unboundedFollowing)
result = (
    totals
    .withColumn("revenue_pct", F.round(F.col("total_revenue") * 100.0 / F.sum("total_revenue").over(w), 2))
    .orderBy(F.desc("revenue_pct"))
)
result.toPandas().to_csv(str(Path(__file__).parent / "expected.csv"), index=False)
print("expected.csv written.")
