import pyspark
from pyspark.sql import SparkSession
import os
import argparse
from pyspark.sql.types import StructType, StructField, StringType
from datetime import datetime, timedelta
from pyspark.sql.functions import current_timestamp, current_date

# Get the current date
current_date_x = datetime.now()

# Calculate the previous date (T-1), which is one day before the current date
previous_date = current_date_x - timedelta(days=1)

# Extract and format year, month, and day for the current date
current_year = current_date_x.year
current_month = f"{current_date_x.month:02}"
current_day = f"{current_date_x.day:02}"

# Extract and format year, month, and day for the previous date
previous_year = previous_date.year
previous_month = f"{previous_date.month:02}"
previous_day = f"{previous_date.day:02}"

# Output the results
print(f"Current Date -> Year: {current_year}, Month: {current_month}, Day: {current_day}")
print(f"Previous Date (T-1) -> Year: {previous_year}, Month: {previous_month}, Day: {previous_day}")


def spark_glue_ice_connection_check(AWS_ACCESS_KEY, AWS_SECRET_KEY, year, month, day):
    # Glue Configurations
    conf = (
        pyspark.SparkConf()
        .setAppName('AWS Glue Iceberg Connection')
        # packages
        .set('spark.jars.packages',
             'org.apache.iceberg:iceberg-spark-runtime-3.4_2.12:1.6.1,org.apache.iceberg:iceberg-aws-bundle:1.5.0,org.apache.hadoop:hadoop-aws:3.3.4')
        # SQL Extensions
        .set('spark.sql.extensions', 'org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions')
        # Configuring Catalog
        .set('spark.sql.catalog.spark_catalog', 'org.apache.iceberg.spark.SparkCatalog')
        .set('spark.sql.catalog.spark_catalog.type', 'glue')
        # AWS Glue Configurations
        .set('spark.sql.catalog.spark_catalog.glue.catalog-endpoint',
             'glue.ap-south-1.amazonaws.com')  # endpoint URL of Glue Catalog
        .set('spark.sql.catalog.spark_catalog.glue.region', 'ap-south-1')  # AWS region
        # S3 Storage
        .set('spark.sql.catalog.spark_catalog.warehouse',
             "s3a://granica-iceberg")  # replace with your S3 bucket path
        .set('spark.hadoop.fs.s3a.access.key', AWS_ACCESS_KEY)
        .set('spark.hadoop.fs.s3a.secret.key', AWS_SECRET_KEY)
        .set("spark.driver.memory", "8g")
        .set("spark.executor.memory", "16g")
        .set("spark.executor.cores", "4")
        .set("spark.sql.shuffle.partitions", "200")
        .set("spark.memory.fraction", "0.8")
        .set("spark.memory.storageFraction", "0.5")
    )
    ## Start Spark Session
    spark = SparkSession.builder.config(conf=conf).getOrCreate()
    spark.conf.set("spark.sql.iceberg.write.target-file-size-bytes", "67108864")  # 32MB
    spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.access.key", AWS_ACCESS_KEY)
    spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.secret.key", AWS_SECRET_KEY)

    spark.sql("select 1;")

    try:
        spark.sql("""select current_schema();""").show()
        schema = StructType([
                                StructField("data", StringType(), True) 
                            ])

        # df = spark.read.schema(schema).text(f"s3a://granica-logs/year={year}/month={month}/day={day}/*/*.txt")
        df = spark.read.schema(schema).text(f"s3a://granica-logs/*/*/*/*/*.txt")
        df.show()
        df = df.withColumn("insertedAt", current_timestamp())
        df = df.withColumn("recordContentDt", current_date())
        df.createOrReplaceTempView('source')
        recordContentDt = df.head(1)[0]["recordContentDt"]
        table_count = spark.sql("""SHOW TABLES IN default like 'log_transformed_iceberg';""").collect()
        if table_count: 
            print("table already exists")
            spark.sql(f"""INSERT
                                OVERWRITE default.log_transformed_iceberg
                                PARTITION
                                (recordContentDt = '{recordContentDt}')
                                SELECT
                                `data`,
                                `insertedAt`
                                FROM
                                source;
                        """
                    )
        else:
            print("table is not their")
            spark.sql("""CREATE OR REPLACE TABLE default.log_transformed_iceberg
                        USING iceberg
                        PARTITIONED BY ( recordContentDt )
                        LOCATION 's3a://granica-iceberg/log_transformed_iceberg'
                        AS SELECT * FROM source
                        """
                    )
        print("Run successfully completed")
    finally:
        spark.stop()
                                                                                                                                               
def main():
    parser = argparse.ArgumentParser(description='Fetch data ')
    parser.add_argument('--AWS_ACCESS_KEY_ID', type=str, help='AWS_ACCESS_KEY_ID')
    parser.add_argument('--AWS_SECRET_ACCESS_KEY', type=str, help='AWS_SECRET_ACCESS_KEY')
    args = parser.parse_args()
    endpoint = args.AWS_ACCESS_KEY_ID
    private_key_file_pwd = args.AWS_SECRET_ACCESS_KEY
    os.environ['AWS_ACCESS_KEY_ID'] = endpoint
    os.environ['AWS_SECRET_ACCESS_KEY_ID'] = private_key_file_pwd
    os.environ['AWS_SECRET_ACCESS_KEY'] = private_key_file_pwd
    os.environ['AWS_REGION'] = 'ap-south-1'
    AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY_ID")  ## AWS CREDENTIALS
    AWS_SECRET_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY_ID")  ## AWS CREDENTIALS

    spark_glue_ice_connection_check(AWS_ACCESS_KEY, AWS_SECRET_KEY, current_year, current_month, current_day)


if __name__ == '__main__':
    main()