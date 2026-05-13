from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pathlib import Path

spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()
BASE = "/problems/customers_above_avg"

df = spark.read.option("header", True).option("inferSchema", True).csv(f"{BASE}/fixture.csv")

totals = (
    df
    .groupBy("customer_id")
    .agg(F.sum("amount").alias("total_spend"))
)

avg_spend = totals.agg(F.avg("total_spend")).collect()[0][0]

result = (
    totals
    .filter(F.col("total_spend") > avg_spend)
    .orderBy(F.col("total_spend").desc())
)

result.toPandas().to_csv(str(Path(__file__).parent / "expected.csv"), index=False)
print("expected.csv written.")
