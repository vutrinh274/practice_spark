from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window
from pathlib import Path

spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()

BASE = "/problems/ledger_reconciliation"

system_ledger = spark.read.csv(f"{BASE}/system_ledger.csv", header=True, inferSchema=True)
bank_ledger   = spark.read.csv(f"{BASE}/bank_ledger.csv",   header=True, inferSchema=True)

sys_df  = system_ledger.select(F.col("txn_id"), F.col("amount").alias("system_amount"))
bank_df = bank_ledger.select(F.col("txn_id"), F.col("amount").alias("bank_amount"))

joined = sys_df.join(bank_df, on="txn_id", how="full")

result = (
    joined
    .withColumn("variance", F.col("bank_amount") - F.col("system_amount"))
    .filter(
        (F.col("system_amount") != F.col("bank_amount"))
        | F.col("system_amount").isNull()
        | F.col("bank_amount").isNull()
    )
    .select("txn_id", "system_amount", "bank_amount", "variance")
    .orderBy("txn_id")
)

result.toPandas().to_csv(str(Path(__file__).parent / "expected.csv"), index=False)
print("expected.csv written.")
