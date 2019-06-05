/*---
check: duration
name: long-connection
status: clear
threshold: 3600
---*/
  WITH c AS (
SELECT extract(epoch FROM age(clock_timestamp(), query_start)) AS duration
     , pid
     , usename
     , application_name
     , state
     , left(query, 80) AS query
  FROM pg_stat_activity
 WHERE backend_type = 'client backend'
   AND query_start IS NOT NULL
 ORDER BY 1 DESC
 LIMIT 1)
SELECT *
  FROM c
 UNION
SELECT 0, -1, NULL, NULL, 'idle', ''
 WHERE NOT EXISTS (SELECT * from c)
;