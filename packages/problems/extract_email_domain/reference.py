from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pathlib import Path
from pyspark.sql.types import StructType, StructField, IntegerType, StringType

spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()
BASE = "/problems/extract_email_domain"

schema = StructType([
    StructField("user_id", IntegerType()),
    StructField("name", StringType()),
    StructField("email", StringType()),
])
df = spark.read.option("header", True).schema(schema).csv(f"{BASE}/fixture.csv")

result = (
    df
    .withColumn("domain", F.regexp_extract(F.col("email"), "@(.+)$", 1))
    .select("user_id", "name", "email", "domain")
    .orderBy("user_id")
)
result.toPandas().to_csv(str(Path(__file__).parent / "expected.csv"), index=False)
print("expected.csv written.")
