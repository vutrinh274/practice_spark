from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window
from pathlib import Path
from pyspark.sql.types import StructType, StructField, IntegerType, StringType

spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()
BASE = "/problems/most_common_tag"

schema = StructType([
    StructField("article_id", IntegerType()),
    StructField("title", StringType()),
    StructField("category", StringType()),
    StructField("tags", StringType()),
])
df = spark.read.option("header", True).schema(schema).csv(f"{BASE}/fixture.csv")

exploded = df.select("category", F.explode(F.split("tags", ",")).alias("tag"))

counts = exploded.groupBy("category", "tag").agg(F.count("*").alias("tag_count"))

w = Window.partitionBy("category").orderBy(F.col("tag_count").desc())

result = (
    counts
    .withColumn("rnk", F.rank().over(w))
    .filter(F.col("rnk") == 1)
    .select("category", "tag", "tag_count")
    .orderBy("category")
)
result.toPandas().to_csv(str(Path(__file__).parent / "expected.csv"), index=False)
print("expected.csv written.")
