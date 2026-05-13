from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pathlib import Path

spark = SparkSession.builder.remote("sc://localhost:15002").getOrCreate()
BASE = "/problems/full_outer_join"

employees = spark.read.option("header", True).option("inferSchema", True).csv(f"{BASE}/employees.csv")
departments = spark.read.option("header", True).option("inferSchema", True).csv(f"{BASE}/departments.csv")

result = (
    employees
    .join(departments, on="department_id", how="outer")
    .select("employee_id", "name", "department_id", "department_name", "budget")
    .orderBy(F.asc_nulls_last("department_id"), F.asc_nulls_last("employee_id"))
)

import pandas as pd
pdf = result.toPandas()
# Convert float columns back to nullable int to avoid "1.0" in CSV
for col in ["employee_id", "department_id", "budget"]:
    if col in pdf.columns:
        pdf[col] = pd.array(pdf[col], dtype=pd.Int64Dtype())
pdf.to_csv(str(Path(__file__).parent / "expected.csv"), index=False)
print("expected.csv written.")
