from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window
from pathlib import Path

spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()
BASE = "/problems/flatten_structs"

df = spark.read.option("header", True).option("inferSchema", True)\
    .option("quote", '"').option("escape", '"').csv(f"{BASE}/fixture.csv")

json_schema = "struct<street:string,city:string,zip:string>"

result = (
    df
    .withColumn("addr", F.from_json(F.col("address"), json_schema))
    .select(
        "order_id",
        "customer_name",
        F.col("addr.street").alias("street"),
        F.col("addr.city").alias("city"),
        F.col("addr.zip").alias("zip"),
        "items_count",
    )
    .orderBy("order_id")
)

result.toPandas().to_csv(str(Path(__file__).parent / "expected.csv"), index=False)
print("expected.csv written.")
