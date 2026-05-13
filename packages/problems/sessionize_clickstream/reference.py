from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window
from pathlib import Path

spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()

BASE = "/problems/sessionize_clickstream"

clickstream = spark.read.csv(f"{BASE}/fixture.csv", header=True, inferSchema=True)

w = Window.partitionBy("user_id").orderBy("event_time")
w_running = Window.partitionBy("user_id").orderBy("event_time").rowsBetween(
    Window.unboundedPreceding, Window.currentRow
)

result = (
    clickstream
    .withColumn("prev_time", F.lag("event_time", 1).over(w))
    .withColumn(
        "gap_secs",
        F.unix_timestamp("event_time") - F.unix_timestamp("prev_time")
    )
    .withColumn(
        "new_flag",
        F.when(
            F.col("prev_time").isNull() | (F.col("gap_secs") > 1800), 1
        ).otherwise(0)
    )
    .withColumn("session_id", F.sum("new_flag").over(w_running))
    .select("event_id", "user_id", "page", "event_time", "session_id")
    .orderBy("user_id", "event_time")
)

result.toPandas().to_csv(str(Path(__file__).parent / "expected.csv"), index=False)
print("expected.csv written.")
