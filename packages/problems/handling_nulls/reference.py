from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pathlib import Path

spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()
CONTAINER_BASE = "/problems/handling_nulls"

df = spark.read.option("header", True).option("inferSchema", True).csv(f"{CONTAINER_BASE}/fixture.csv")

result = (
    df
    .fillna({"department": "Unknown", "salary": 0})
    .filter(F.col("salary") > 0)
    .select("employee_id", "name", "department", "salary")
    .orderBy("employee_id")
)

result.toPandas().to_csv(str(Path(__file__).parent / "expected.csv"), index=False)
print("expected.csv written.")
