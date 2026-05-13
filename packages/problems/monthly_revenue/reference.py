from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pathlib import Path

spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()
BASE = "/problems/monthly_revenue"
from pyspark.sql.types import StructType, StructField, IntegerType, StringType
schema = StructType([
    StructField("order_id", IntegerType()),
    StructField("order_date", StringType()),
    StructField("amount", IntegerType()),
    StructField("category", StringType()),
])
df = spark.read.option("header", True).schema(schema).csv(f"{BASE}/fixture.csv")

result = (
    df
    .withColumn("month", F.date_format(F.col("order_date"), "yyyy-MM"))
    .groupBy("month")
    .agg(F.sum("amount").alias("total_revenue"), F.count("*").alias("num_orders"))
    .orderBy("month")
)
result.toPandas().to_csv(str(Path(__file__).parent / "expected.csv"), index=False)
print("expected.csv written.")
