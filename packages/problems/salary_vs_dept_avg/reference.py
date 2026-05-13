from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window
from pathlib import Path

spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()
BASE = "/problems/salary_vs_dept_avg"

df = spark.read.option("header", True).option("inferSchema", True).csv(f"{BASE}/fixture.csv")

w = Window.partitionBy("department")

result = (
    df
    .withColumn("dept_avg_salary", F.round(F.avg("salary").over(w), 2))
    .withColumn("diff_from_avg", F.round(F.col("salary") - F.avg("salary").over(w), 2))
    .select("employee_id", "name", "department", "salary", "dept_avg_salary", "diff_from_avg")
    .orderBy("department", "employee_id")
)

result.toPandas().to_csv(str(Path(__file__).parent / "expected.csv"), index=False)
print("expected.csv written.")
