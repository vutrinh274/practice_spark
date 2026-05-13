from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pathlib import Path
from pyspark.sql.types import StructType, StructField, IntegerType, StringType

spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()
BASE = "/problems/late_deliveries"

schema = StructType([
    StructField("order_id", IntegerType()),
    StructField("customer_id", IntegerType()),
    StructField("order_date", StringType()),
    StructField("delivery_date", StringType()),
    StructField("promised_days", IntegerType()),
])
df = spark.read.option("header", True).schema(schema).csv(f"{BASE}/fixture.csv")

result = (
    df
    .withColumn("actual_days", F.datediff(F.col("delivery_date"), F.col("order_date")))
    .withColumn("days_late", F.col("actual_days") - F.col("promised_days"))
    .filter(F.col("actual_days") > F.col("promised_days"))
    .select("order_id", "customer_id", "promised_days", "actual_days", "days_late")
    .orderBy(F.col("days_late").desc())
)
result.toPandas().to_csv(str(Path(__file__).parent / "expected.csv"), index=False)
print("expected.csv written.")
