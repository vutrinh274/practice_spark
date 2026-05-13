from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pathlib import Path

spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()
BASE = "/problems/self_join_manager"

df = spark.read.option("header", True).option("inferSchema", True).csv(f"{BASE}/fixture.csv")

managers = df.select(
    F.col("employee_id").alias("manager_id"),
    F.col("name").alias("manager_name")
)

result = (
    df
    .join(managers, on="manager_id", how="left")
    .select("employee_id", "name", "department", "manager_name")
    .orderBy("employee_id")
)

result.toPandas().to_csv(str(Path(__file__).parent / "expected.csv"), index=False)
print("expected.csv written.")
