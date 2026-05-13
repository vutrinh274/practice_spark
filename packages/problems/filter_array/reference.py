from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pathlib import Path
from pyspark.sql.types import StructType, StructField, IntegerType, StringType

spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()
BASE = "/problems/filter_array"

schema = StructType([
    StructField("user_id", IntegerType()),
    StructField("name", StringType()),
    StructField("interests", StringType()),
])
df = spark.read.option("header", True).schema(schema).csv(f"{BASE}/fixture.csv")

result = (
    df
    .filter(F.array_contains(F.split(F.col("interests"), ","), "Technology"))
    .select("user_id", "name")
    .orderBy("user_id")
)
result.toPandas().to_csv(str(Path(__file__).parent / "expected.csv"), index=False)
print("expected.csv written.")
