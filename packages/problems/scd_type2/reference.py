from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window
from pathlib import Path

spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()
BASE = "/problems/scd_type2"

df = spark.read.option("header", True).option("inferSchema", True).csv(f"{BASE}/fixture.csv")

w = Window.partitionBy("employee_id").orderBy("effective_date")

result = (
    df
    .withColumn("end_date", F.lead("effective_date").over(w))
    .withColumn("is_current", F.when(F.col("end_date").isNull(), 1).otherwise(0))
    .select(
        "record_id",
        "employee_id",
        "name",
        "department",
        "salary",
        "effective_date",
        "end_date",
        "is_current",
    )
    .orderBy("employee_id", "effective_date")
)

result.toPandas().to_csv(str(Path(__file__).parent / "expected.csv"), index=False)
print("expected.csv written.")
