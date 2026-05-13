from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pathlib import Path

spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()
BASE = "/problems/customers_no_orders"

customers = spark.read.option("header", True).option("inferSchema", True).csv(f"{BASE}/customers.csv")
orders = spark.read.option("header", True).option("inferSchema", True).csv(f"{BASE}/orders.csv")

result = (
    customers
    .join(orders, on="customer_id", how="left_anti")
    .select("customer_id", "name", "city", "signup_date")
    .orderBy("customer_id")
)

result.toPandas().to_csv(str(Path(__file__).parent / "expected.csv"), index=False)
print("expected.csv written.")
