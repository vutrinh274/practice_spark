from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window
from pathlib import Path

spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()

BASE = "/problems/customer_loyalty"

orders  = spark.read.csv(f"{BASE}/orders.csv",  header=True, inferSchema=True)
ratings = spark.read.csv(f"{BASE}/ratings.csv", header=True, inferSchema=True)

order_stats = (
    orders
    .groupBy("customer_id")
    .agg(
        F.count("*").alias("total_orders"),
        F.round(F.avg("amount"), 2).alias("avg_order_value"),
    )
)

rating_stats = (
    ratings
    .groupBy("customer_id")
    .agg(F.round(F.avg("score"), 2).alias("avg_rating"))
)

result = (
    order_stats
    .join(rating_stats, on="customer_id")
    .withColumn(
        "loyalty_score",
        F.round(
            F.col("total_orders") * 0.3
            + F.col("avg_order_value") * 0.5
            + F.col("avg_rating") * 0.2,
            2,
        )
    )
    .select("customer_id", "total_orders", "avg_order_value", "avg_rating", "loyalty_score")
    .orderBy(F.col("loyalty_score").desc())
)

result.toPandas().to_csv(str(Path(__file__).parent / "expected.csv"), index=False)
print("expected.csv written.")
