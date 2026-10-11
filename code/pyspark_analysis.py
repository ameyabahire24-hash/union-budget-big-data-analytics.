"""Exploratory PySpark analysis for the Union Budget project.

Before running, reconstruct the CSV from data/dataset_csv_gzip_b64_part_*.txt:
    python code/restore_dataset.py
Then run:
    python code/pyspark_analysis.py

The source table is preliminary. Keep nulls as nulls and do not infer official totals
until records are reconciled against source PDFs.
"""
from pathlib import Path
from pyspark.sql import SparkSession, functions as F
from pyspark.sql.window import Window

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "data" / "Union_Budget_Analytical_Dataset.csv"

spark = SparkSession.builder.appName("UnionBudgetBigDataAnalytics").getOrCreate()
df = (spark.read.option("header", True).option("inferSchema", True)
      .csv(str(path)))
df.printSchema()
df.show(5, truncate=False)

numeric = ["Revenue_Cr", "Capital_Cr", "Total_Cr"]
df.select([
    F.sum(F.col(c).isNull().cast("int")).alias(f"{c}_missing")
    for c in numeric
]).show()

df.groupBy("Financial_Year").agg(
    F.count("*").alias("rows"),
    F.count("Total_Cr").alias("non_null_total_rows"),
    F.sum("Total_Cr").alias("recorded_total_cr")
).orderBy("Financial_Year").show(truncate=False)

df.groupBy("Financial_Year", "Demand_No").count().filter(
    F.col("count") > 1
).show()

df.groupBy("Demand_or_Department").agg(
    F.count("Total_Cr").alias("observations"),
    F.min("Total_Cr").alias("min_cr"),
    F.max("Total_Cr").alias("max_cr"),
    F.avg("Total_Cr").alias("mean_cr"),
    F.stddev("Total_Cr").alias("stddev_cr")
).orderBy(F.desc("max_cr")).show(20, truncate=False)

annual = df.groupBy("Financial_Year").agg(
    F.sum("Total_Cr").alias("recorded_total_cr")
).orderBy("Financial_Year")
w = Window.orderBy("Financial_Year")
annual = (annual.withColumn("previous_recorded_total", F.lag("recorded_total_cr").over(w))
          .withColumn("change_cr", F.col("recorded_total_cr") - F.col("previous_recorded_total"))
          .withColumn("change_pct",
                      (F.col("recorded_total_cr") / F.col("previous_recorded_total") - 1) * 100))
annual.show(truncate=False)

spark.stop()
