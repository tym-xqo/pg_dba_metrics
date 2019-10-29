---
status: clear
threshold:
  field: duration
  gate: 300
---
WITH d AS (
SELECT extract(epoch FROM age(clock_timestamp(), query_start)) AS duration
     , pid
     , usename
     , application_name
     , state
     , left(query, 80) AS query
  FROM pg_stat_activity
 WHERE backend_type = 'client backend'
   AND state != 'idle'
   AND application_name != 'pg_dba_metrics'
 ORDER BY 1 DESC
 LIMIT 1)
SELECT * 
  FROM d
 UNION
SELECT 0, -1, NULL, NULL, 'idle', ''
 WHERE NOT EXISTS (SELECT *
                     FROM d)
;
