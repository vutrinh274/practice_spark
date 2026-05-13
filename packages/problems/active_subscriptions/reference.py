from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pathlib import Path
from pyspark.sql.types import StructType, StructField, IntegerType, StringType

spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()
BASE = "/problems/active_subscriptions"

schema = StructType([
    StructField("sub_id", IntegerType()),
    StructField("customer_id", IntegerType()),
    StructField("start_date", StringType()),
    StructField("end_date", StringType()),
    StructField("plan", StringType()),
])
df = spark.read.option("header", True).schema(schema).csv(f"{BASE}/fixture.csv")

target_date = "2024-06-15"

result = (
    df
    .filter(
        (F.col("start_date") <= target_date) &
        (F.col("end_date") >= target_date)
    )
    .select("sub_id", "customer_id", "plan", "start_date", "end_date")
    .orderBy("sub_id")
)
result.toPandas().to_csv(str(Path(__file__).parent / "expected.csv"), index=False)
print("expected.csv written.")
