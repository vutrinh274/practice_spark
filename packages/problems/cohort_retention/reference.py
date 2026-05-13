from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window
from pathlib import Path

spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()
BASE = "/problems/cohort_retention"

df = spark.read.option("header", True).option("inferSchema", True).csv(f"{BASE}/fixture.csv")

result = (
    df
    .withColumn("cohort_month", F.date_format(F.col("signup_date"), "yyyy-MM"))
    .withColumn(
        "months_since_signup",
        F.months_between(
            F.to_date(F.col("activity_date")),
            F.to_date(F.col("signup_date"))
        ).cast("int")
    )
    .filter((F.col("months_since_signup") >= 0) & (F.col("months_since_signup") <= 3))
    .groupBy("cohort_month", "months_since_signup")
    .agg(F.countDistinct("user_id").alias("active_users"))
    .orderBy("cohort_month", "months_since_signup")
)

result.toPandas().to_csv(str(Path(__file__).parent / "expected.csv"), index=False)
print("expected.csv written.")
