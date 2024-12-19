import argparse
import logging
import sys
import os

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType
from datetime import datetime, timedelta
from pyspark.sql.functions import current_timestamp, current_date


def init_spark():
    return SparkSession.builder.appName("execute_file_w_db.py").getOrCreate()




def main():
    logger = logging.getLogger(__name__)
    spark = init_spark()
    try:
        spark.sql("select 1;")
        schema = StructType([
                                StructField("data", StringType(), True) 
                            ])
        spark.sql("""select current_schema();""").show()
        df = spark.read.schema(schema).text(f"s3a://granica-logs/year=2024/month=12/day=18/hour=00/download.txt")
        df.show()
        df.createOrReplaceTempView('content_day_wise')
        df = df.withColumn("insertedAt", current_timestamp())
        df = df.withColumn("recordContentDt", current_date())
        df.show()
        spark.sql("select count(*) from default.log_transformed_iceberg").show()

    except Exception as e:
        statement = f"sqlfile failed with {e}"
        print(statement)
        logger.error(statement)
        raise e
    finally:
        spark.stop()


if __name__ == "__main__":
    main()