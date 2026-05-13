from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pathlib import Path

spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()
BASE = "/problems/simple_inner_join"

orders = spark.read.option("header", True).option("inferSchema", True).csv(f"{BASE}/orders.csv")
customers = spark.read.option("header", True).option("inferSchema", True).csv(f"{BASE}/customers.csv")

result = (
    orders
    .filter(F.col("status") == "completed")
    .join(customers, on="customer_id")
    .select("order_id", "name", "city", "amount")
    .orderBy("order_id")
)

result.toPandas().to_csv(str(Path(__file__).parent / "expected.csv"), index=False)
print("expected.csv written.")
