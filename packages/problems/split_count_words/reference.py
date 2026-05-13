from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pathlib import Path
from pyspark.sql.types import StructType, StructField, IntegerType, StringType

spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()
BASE = "/problems/split_count_words"

schema = StructType([
    StructField("review_id", IntegerType()),
    StructField("product_id", IntegerType()),
    StructField("review_text", StringType()),
])
df = spark.read.option("header", True).schema(schema).csv(f"{BASE}/fixture.csv")

stop_words = ["the", "and", "for", "this", "was", "very", "are", "with", "that"]

result = (
    df
    .select(F.explode(F.split(F.col("review_text"), " ")).alias("word_raw"))
    .select(F.lower(F.trim(F.col("word_raw"))).alias("word"))
    .filter(F.length(F.col("word")) >= 3)
    .filter(~F.col("word").isin(stop_words))
    .groupBy("word")
    .agg(F.count("*").alias("count"))
    .orderBy(F.col("count").desc(), F.col("word").asc())
    .limit(5)
)

result.toPandas().to_csv(str(Path(__file__).parent / "expected.csv"), index=False)
print("expected.csv written.")
