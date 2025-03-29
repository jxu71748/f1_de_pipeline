from pyspark.sql import SparkSession
from pyspark.sql.functions import col, concat_ws, to_timestamp, when
from pyspark.sql.types import IntegerType, FloatType
import os


def snake_case(s):
    return s.replace(" ", "_").replace("-", "_").lower()

def transform_csv_to_parquet(input_dir, output_dir):
    spark = SparkSession.builder \
        .appName("F1 Data Transformation") \
        .getOrCreate()

    os.makedirs(output_dir, exist_ok=True)

    for csv_file in os.listdir(input_dir):
        if csv_file.endswith(".csv"):
            file_name = csv_file.replace(".csv", "")
            df = spark.read.option("header", True).csv(os.path.join(input_dir, csv_file))

            # Unified field names
            for old_name in df.columns:
                df = df.withColumnRenamed(old_name, snake_case(old_name))

            # Replace "\N" to None
            df = df.replace("\\N", None)

            # Drop duplicates and all-null rows
            df = df.dropDuplicates().na.drop("all")

            # races.csv: Merge date + time to race_timestamp
            if file_name == "races":
                if "date" in df.columns and "time" in df.columns:
                    df = df.withColumn("race_timestamp", to_timestamp(concat_ws(" ", col("date"), col("time")))) \
                           .drop("date", "time")

            # Type casting
            if "milliseconds" in df.columns:
                df = df.withColumn("milliseconds", col("milliseconds").cast(IntegerType()))

            if "points" in df.columns:
                df = df.withColumn("points", col("points").cast(FloatType()))

            # Force xxxId fields to IntegerType
            for c in df.columns:
                if c.lower().endswith("id"):
                    df = df.withColumn(c, when(col(c).rlike("^\\d+$"), col(c).cast(IntegerType())).otherwise(None))

            # Output to Parquet
            output_path = os.path.join(output_dir, f"{file_name}.parquet")
            df.write.mode("overwrite").parquet(output_path)
            print(f"Transformed and saved: {file_name} → {output_path}")

    spark.stop()

if __name__ == "__main__":
    input_dir = "/opt/airflow/raw_data"
    output_dir = "/opt/airflow/data/transformed"
    transform_csv_to_parquet(input_dir, output_dir)
