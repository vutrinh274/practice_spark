from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window
from pathlib import Path

spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()

CONTAINER_BASE = "/problems/running_total"

orders = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(f"{CONTAINER_BASE}/fixture.csv")
)

window = (
    Window
    .partitionBy("customer_id")
    .orderBy("order_date")
    .rowsBetween(Window.unboundedPreceding, Window.currentRow)
)

result = (
    orders
    .withColumn("running_total", F.sum("amount").over(window))
    .select("customer_id", "order_date", "amount", "running_total")
    .orderBy("customer_id", "order_date")
)

result.toPandas().to_csv(str(Path(__file__).parent / "expected.csv"), index=False)
print("expected.csv written.")
