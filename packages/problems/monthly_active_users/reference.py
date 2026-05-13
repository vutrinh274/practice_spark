from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pathlib import Path
from pyspark.sql.types import StructType, StructField, IntegerType, StringType

spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()
BASE = "/problems/monthly_active_users"

schema = StructType([
    StructField("user_id", IntegerType()),
    StructField("activity_date", StringType()),
    StructField("action", StringType()),
])
df = spark.read.option("header", True).schema(schema).csv(f"{BASE}/fixture.csv")

result = (
    df
    .withColumn("month", F.date_format(F.col("activity_date"), "yyyy-MM"))
    .groupBy("month")
    .agg(F.countDistinct("user_id").alias("active_users"))
    .orderBy("month")
)
result.toPandas().to_csv(str(Path(__file__).parent / "expected.csv"), index=False)
print("expected.csv written.")
