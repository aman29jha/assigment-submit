INSERT
  OVERWRITE {database}.{table}
PARTITION
  (recordContentDt = '{recordContentDt}')
SELECT
  `data`,
  `insertedAt`,
  `recordContentDt`
FROM
  source;