---
status: clear
threshold:
  field: duration
  gate: 30
---
  WITH w AS(
SELECT extract(epoch FROM max(age(clock_timestamp(), query_start))) AS duration,
       wait_event_type,
       pid
  FROM pg_stat_activity
 WHERE backend_type = 'client backend'
   AND wait_event_type IS NOT NULL
   AND query_start IS NOT NULL
   AND state != 'idle'
   AND application_name != 'pg_dba_metrics'
 GROUP BY 2, 3
 ORDER BY 1 DESC
 LIMIT 1)
SELECT * from w
 UNION
SELECT 0, 'none', -1
 WHERE NOT EXISTS (SELECT * FROM w)