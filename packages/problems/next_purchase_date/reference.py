from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window
from pathlib import Path

spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()
BASE = "/problems/next_purchase_date"

df = spark.read.option("header", True).option("inferSchema", True).csv(f"{BASE}/fixture.csv")

w = Window.partitionBy("customer_id").orderBy("purchase_date")

result = (
    df
    .withColumn("next_purchase_date", F.lead("purchase_date", 1).over(w))
    .select("purchase_id", "customer_id", "purchase_date", "next_purchase_date")
    .orderBy("customer_id", "purchase_date")
)

result.toPandas().to_csv(str(Path(__file__).parent / "expected.csv"), index=False)
print("expected.csv written.")
