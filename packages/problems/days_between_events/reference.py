from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pathlib import Path
from pyspark.sql.types import StructType, StructField, IntegerType, StringType

spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()
BASE = "/problems/days_between_events"

schema = StructType([
    StructField("event_id", IntegerType()),
    StructField("user_id", IntegerType()),
    StructField("event_type", StringType()),
    StructField("event_date", StringType()),
])
df = spark.read.option("header", True).schema(schema).csv(f"{BASE}/fixture.csv")

pivoted = (
    df
    .groupBy("user_id")
    .agg(
        F.max(F.when(F.col("event_type") == "signup", F.col("event_date"))).alias("signup_date"),
        F.max(F.when(F.col("event_type") == "first_purchase", F.col("event_date"))).alias("first_purchase_date"),
    )
)

result = (
    pivoted
    .withColumn("days_to_purchase", F.datediff(F.col("first_purchase_date"), F.col("signup_date")))
    .select("user_id", "signup_date", "first_purchase_date", "days_to_purchase")
    .orderBy("user_id")
)
result.toPandas().to_csv(str(Path(__file__).parent / "expected.csv"), index=False)
print("expected.csv written.")
