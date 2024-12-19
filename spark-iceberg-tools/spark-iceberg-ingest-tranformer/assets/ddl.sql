create table if not exists {database}.{table} (
  `data` string,
  `insertedAt` timestamp,
  `recordContentDt` date
) using iceberg partitioned by (recordContentDt);