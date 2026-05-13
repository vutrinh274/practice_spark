from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window
from pyspark.sql import Row
from pathlib import Path

spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()

BASE = "/problems/funnel_analysis"

user_events = spark.read.csv(f"{BASE}/fixture.csv", header=True, inferSchema=True)

stage_map = spark.createDataFrame([
    Row(stage="view",     stage_order=1),
    Row(stage="cart",     stage_order=2),
    Row(stage="checkout", stage_order=3),
    Row(stage="purchase", stage_order=4),
])

counts = (
    user_events
    .groupBy(F.col("event_type").alias("stage"))
    .agg(F.countDistinct("user_id").alias("users_reached"))
)

result = (
    counts
    .join(stage_map, on="stage")
    .select("stage", "stage_order", "users_reached")
    .orderBy("stage_order")
)

result.toPandas().to_csv(str(Path(__file__).parent / "expected.csv"), index=False)
print("expected.csv written.")
