from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pathlib import Path
from pyspark.sql.types import StructType, StructField, IntegerType, StringType

spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()
BASE = "/problems/standardize_phones"

schema = StructType([
    StructField("contact_id", IntegerType()),
    StructField("name", StringType()),
    StructField("phone", StringType()),
])
df = spark.read.option("header", True).schema(schema).csv(f"{BASE}/fixture.csv")

result = (
    df
    .withColumn("original_phone", F.col("phone"))
    .withColumn("digits", F.regexp_replace(F.col("phone"), "[^0-9]", ""))
    .withColumn(
        "standardized_phone",
        F.concat(
            F.substring(F.col("digits"), 1, 3),
            F.lit("-"),
            F.substring(F.col("digits"), 4, 3),
            F.lit("-"),
            F.substring(F.col("digits"), 7, 4),
        )
    )
    .select("contact_id", "name", "original_phone", "standardized_phone")
    .orderBy("contact_id")
)

result.toPandas().to_csv(str(Path(__file__).parent / "expected.csv"), index=False)
print("expected.csv written.")
