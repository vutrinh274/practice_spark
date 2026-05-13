from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window
from pathlib import Path

spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()

BASE = "/problems/consecutive_streaks"

attendance = spark.read.csv(f"{BASE}/fixture.csv", header=True, inferSchema=True)

w = Window.partitionBy("employee_id").orderBy("attendance_date")

result = (
    attendance
    .filter(F.col("status") == "Present")
    .withColumn("rn", F.row_number().over(w))
    .withColumn("grp", F.date_sub(F.col("attendance_date"), F.col("rn")))
    .groupBy("employee_id", "grp")
    .agg(F.count("*").alias("streak_len"))
    .groupBy("employee_id")
    .agg(F.max("streak_len").alias("max_streak"))
    .orderBy("employee_id")
)

result.toPandas().to_csv(str(Path(__file__).parent / "expected.csv"), index=False)
print("expected.csv written.")
