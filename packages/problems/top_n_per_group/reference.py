from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window
from pathlib import Path

spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()

CONTAINER_BASE = "/problems/top_n_per_group"

employees = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(f"{CONTAINER_BASE}/fixture.csv")
)

window = Window.partitionBy("department").orderBy(F.desc("salary"))

result = (
    employees
    .withColumn("rank", F.rank().over(window))
    .filter(F.col("rank") <= 2)
    .orderBy("department", "rank")
)

result.toPandas().to_csv(str(Path(__file__).parent / "expected.csv"), index=False)
print("expected.csv written.")
