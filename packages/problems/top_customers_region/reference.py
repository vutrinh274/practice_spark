from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window
from pathlib import Path

spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()
BASE = "/problems/top_customers_region"

df = spark.read.option("header", True).option("inferSchema", True).csv(f"{BASE}/fixture.csv")

w = Window.partitionBy("region").orderBy(F.col("total_spend").desc())

result = (
    df
    .withColumn("rank", F.rank().over(w))
    .filter(F.col("rank") <= 2)
    .select("region", "customer_id", "name", "total_spend", "rank")
    .orderBy("region", "rank")
)

result.toPandas().to_csv(str(Path(__file__).parent / "expected.csv"), index=False)
print("expected.csv written.")
