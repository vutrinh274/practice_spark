from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pathlib import Path
from pyspark.sql.types import StructType, StructField, IntegerType, StringType

spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()
BASE = "/problems/mask_pii"

schema = StructType([
    StructField("customer_id", IntegerType()),
    StructField("name", StringType()),
    StructField("email", StringType()),
    StructField("phone", StringType()),
])
df = spark.read.option("header", True).schema(schema).csv(f"{BASE}/fixture.csv")

result = (
    df
    .withColumn(
        "masked_email",
        F.concat(
            F.substring(F.col("email"), 1, 3),
            F.lit("***@"),
            F.regexp_extract(F.col("email"), "@(.+)$", 1),
        )
    )
    .withColumn(
        "masked_phone",
        F.concat(
            F.lit("***-***-"),
            F.substring(F.col("phone"), F.length(F.col("phone")) - 3, 4),
        )
    )
    .select("customer_id", "name", "masked_email", "masked_phone")
    .orderBy("customer_id")
)
result.toPandas().to_csv(str(Path(__file__).parent / "expected.csv"), index=False)
print("expected.csv written.")
