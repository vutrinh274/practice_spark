from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window
from pathlib import Path

spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()

BASE = "/problems/tally_election"

votes = spark.read.csv(f"{BASE}/fixture.csv", header=True, inferSchema=True)

w = Window.partitionBy("district").orderBy(F.col("votes").desc())

result = (
    votes
    .groupBy("district", "candidate")
    .agg(F.count("*").alias("votes"))
    .withColumn("rnk", F.rank().over(w))
    .filter(F.col("rnk") == 1)
    .select("district", "candidate", "votes")
    .orderBy("district")
)

result.toPandas().to_csv(str(Path(__file__).parent / "expected.csv"), index=False)
print("expected.csv written.")
