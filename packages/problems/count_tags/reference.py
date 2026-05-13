from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pathlib import Path
from pyspark.sql.types import StructType, StructField, IntegerType, StringType

spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()
BASE = "/problems/count_tags"

schema = StructType([
    StructField("product_id", IntegerType()),
    StructField("product_name", StringType()),
    StructField("tags", StringType()),
])
df = spark.read.option("header", True).schema(schema).csv(f"{BASE}/fixture.csv")

result = (
    df
    .withColumn("tag_count", F.size(F.split(F.col("tags"), ",")))
    .select("product_id", "product_name", "tag_count")
    .orderBy(F.col("tag_count").desc(), F.col("product_id"))
)
result.toPandas().to_csv(str(Path(__file__).parent / "expected.csv"), index=False)
print("expected.csv written.")
