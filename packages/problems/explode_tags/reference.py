from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pathlib import Path
from pyspark.sql.types import StructType, StructField, IntegerType, StringType

spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()
BASE = "/problems/explode_tags"

schema = StructType([
    StructField("product_id", IntegerType()),
    StructField("product_name", StringType()),
    StructField("tags", StringType()),
])
df = spark.read.option("header", True).schema(schema).csv(f"{BASE}/fixture.csv")

result = (
    df
    .withColumn("tag", F.explode(F.split(F.col("tags"), ",")))
    .select("product_id", "product_name", "tag")
    .orderBy("product_id", "tag")
)
result.toPandas().to_csv(str(Path(__file__).parent / "expected.csv"), index=False)
print("expected.csv written.")
