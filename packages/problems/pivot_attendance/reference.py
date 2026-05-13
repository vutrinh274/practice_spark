from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pathlib import Path

spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()
BASE = "/problems/pivot_attendance"

df = spark.read.option("header", True).option("inferSchema", True).csv(f"{BASE}/fixture.csv")

result = (
    df
    .groupBy("employee_id")
    .pivot("status", ["Present", "Absent", "Late"])
    .count()
    .orderBy("employee_id")
)

result.toPandas().to_csv(str(Path(__file__).parent / "expected.csv"), index=False)
print("expected.csv written.")
