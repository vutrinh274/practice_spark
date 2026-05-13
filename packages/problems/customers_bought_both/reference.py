from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pathlib import Path

spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()
BASE = "/problems/customers_bought_both"

df = spark.read.option("header", True).option("inferSchema", True).csv(f"{BASE}/fixture.csv")

laptop_buyers = df.filter(F.col("product") == "Laptop").select("customer_id")
phone_buyers = df.filter(F.col("product") == "Phone").select("customer_id")

result = laptop_buyers.intersect(phone_buyers).orderBy("customer_id")

result.toPandas().to_csv(str(Path(__file__).parent / "expected.csv"), index=False)
print("expected.csv written.")
