from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pathlib import Path

spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()
BASE = "/problems/remove_outliers"

df = spark.read.option("header", True).option("inferSchema", True).csv(f"{BASE}/fixture.csv")

stats = df.agg(
    F.percentile_approx("amount", 0.25).alias("q1"),
    F.percentile_approx("amount", 0.75).alias("q3")
).collect()[0]

q1, q3 = stats["q1"], stats["q3"]
iqr = q3 - q1
lower = q1 - 1.5 * iqr
upper = q3 + 1.5 * iqr

result = (
    df
    .filter((F.col("amount") >= lower) & (F.col("amount") <= upper))
    .orderBy("transaction_id")
)

result.toPandas().to_csv(str(Path(__file__).parent / "expected.csv"), index=False)
print("expected.csv written.")
