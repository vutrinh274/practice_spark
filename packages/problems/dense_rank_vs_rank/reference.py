from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window
from pathlib import Path

spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()
BASE = "/problems/dense_rank_vs_rank"

df = spark.read.option("header", True).option("inferSchema", True).csv(f"{BASE}/fixture.csv")

w = Window.orderBy(F.col("score").desc())

result = (
    df
    .withColumn("rank", F.rank().over(w))
    .withColumn("dense_rank", F.dense_rank().over(w))
    .select("student_id", "name", "score", "rank", "dense_rank")
    .orderBy(F.col("score").desc(), "student_id")
)

result.toPandas().to_csv(str(Path(__file__).parent / "expected.csv"), index=False)
print("expected.csv written.")
