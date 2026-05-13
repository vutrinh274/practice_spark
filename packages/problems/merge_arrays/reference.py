from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pathlib import Path
from pyspark.sql.types import StructType, StructField, IntegerType, StringType

spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()
BASE = "/problems/merge_arrays"

schema = StructType([
    StructField("user_id", IntegerType()),
    StructField("purchase_date", StringType()),
    StructField("items", StringType()),
])
df = spark.read.option("header", True).schema(schema).csv(f"{BASE}/fixture.csv")

result = (
    df
    .select("user_id", F.explode(F.split(F.col("items"), ",")).alias("item_raw"))
    .select("user_id", F.trim(F.col("item_raw")).alias("item"))
    .groupBy("user_id")
    .agg(F.array_join(F.array_sort(F.collect_set("item")), ",").alias("all_items"))
    .orderBy("user_id")
)
result.toPandas().to_csv(str(Path(__file__).parent / "expected.csv"), index=False)
print("expected.csv written.")
