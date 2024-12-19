import os


def create_table(spark):
  with open(f"/opt/spark/work-dir/spark-iceberg-ingest-transformer/assets/ddl.sql", "r") as file:
    sql_raw = file.read()

  sql_formatted = sql_raw.format_map({
      "database": 'default',
      "table": 'log_analysis'
  })

  print(sql_formatted)

  spark.sql(sql_formatted)


def insert_records(spark, df):
  df.createOrReplaceTempView("source")

  recordContentDt = df.head(1)[0]["recordContentDt"]

  with open(f"/opt/spark/work-dir/spark-iceberg-ingest-transformer/assets/dml.sql", "r") as file:
    sql_raw = file.read()

  sql_formatted = sql_raw.format_map({
      "recordContentDt": recordContentDt,
      "database": 'default',
      "table": 'log_analysis'
  })

  print(sql_formatted)

  spark.sql(sql_formatted)