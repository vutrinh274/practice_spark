# Run once to generate expected.csv
# Usage: make seed
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pathlib import Path

spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()

CONTAINER_BASE = "/problems/group_by_basics"

fixture = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(f"{CONTAINER_BASE}/fixture.csv")
)

result = (
    fixture
    .groupBy("customer_id")
    .agg(F.sum("amount").alias("total_amount"))
)

local_output = Path(__file__).parent / "expected.csv"
result.toPandas().to_csv(str(local_output), index=False)
print(f"expected.csv written to {local_output}")
