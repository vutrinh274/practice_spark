from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pathlib import Path
from pyspark.sql.types import StructType, StructField, IntegerType, StringType

spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()
BASE = "/problems/weekend_vs_weekday"

schema = StructType([
    StructField("sale_id", IntegerType()),
    StructField("sale_date", StringType()),
    StructField("amount", IntegerType()),
])
df = spark.read.option("header", True).schema(schema).csv(f"{BASE}/fixture.csv")

result = (
    df
    .withColumn(
        "day_type",
        F.when(F.dayofweek(F.col("sale_date")).isin(1, 7), "Weekend").otherwise("Weekday")
    )
    .groupBy("day_type")
    .agg(
        F.sum("amount").alias("total_revenue"),
        F.count("*").alias("num_sales")
    )
    .orderBy("day_type")
)
result.toPandas().to_csv(str(Path(__file__).parent / "expected.csv"), index=False)
print("expected.csv written.")
