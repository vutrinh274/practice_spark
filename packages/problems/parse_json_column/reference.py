from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window
from pathlib import Path

spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()
BASE = "/problems/parse_json_column"

df = spark.read.option("header", True).option("inferSchema", True)\
    .option("quote", '"').option("escape", '"').csv(f"{BASE}/fixture.csv")

json_schema = "struct<page:string,duration:string,referrer:string>"

result = (
    df
    .withColumn("parsed", F.from_json(F.col("properties"), json_schema))
    .select(
        "event_id",
        "user_id",
        "event_type",
        F.col("parsed.page").alias("page"),
        F.col("parsed.duration").alias("duration"),
        F.col("parsed.referrer").alias("referrer"),
    )
    .orderBy("event_id")
)

result.toPandas().to_csv(str(Path(__file__).parent / "expected.csv"), index=False)
print("expected.csv written.")
