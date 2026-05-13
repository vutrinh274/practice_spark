from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window
from pathlib import Path

spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()

BASE = "/problems/top_n_tiebreak"

employees = spark.read.csv(f"{BASE}/fixture.csv", header=True, inferSchema=True)

w = Window.partitionBy("department").orderBy(
    F.col("salary").desc(),
    F.col("employee_id").asc(),
)

result = (
    employees
    .withColumn("row_num", F.row_number().over(w))
    .filter(F.col("row_num") <= 2)
    .select("department", "employee_id", "name", "salary", "row_num")
    .orderBy("department", "row_num")
)

result.toPandas().to_csv(str(Path(__file__).parent / "expected.csv"), index=False)
print("expected.csv written.")
