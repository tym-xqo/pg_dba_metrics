/*---
check: avg_duration
status: clear
threshold: 7
---*/
WITH h AS (
        SELECT extract(epoch FROM age(clock_timestamp(), query_start)) AS duration
          FROM pg_stat_activity
         WHERE backend_type = 'client backend'
           AND state != 'idle'
           AND application_name != 'pg_dba_metrics'
       ) 
SELECT coalesce(avg(duration), 0) AS avg_duration
  FROM h;