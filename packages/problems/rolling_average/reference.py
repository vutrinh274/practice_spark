from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window
from pathlib import Path

spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()
BASE = "/problems/rolling_average"

df = spark.read.option("header", True).option("inferSchema", True).csv(f"{BASE}/fixture.csv")

w = Window.orderBy("sale_date").rowsBetween(-6, 0)

result = (
    df
    .withColumn("rolling_avg_7d", F.round(F.avg("amount").over(w), 2))
    .select("sale_date", "amount", "rolling_avg_7d")
    .orderBy("sale_date")
)

result.toPandas().to_csv(str(Path(__file__).parent / "expected.csv"), index=False)
print("expected.csv written.")
