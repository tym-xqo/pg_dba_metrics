/*---
check: duration
status: clear
threshold: 15
---*/
  WITH p AS (
       SELECT DISTINCT pid 
         FROM pg_locks 
        WHERE NOT granted)
SELECT pid
     , pg_blocking_pids(pid)
     , mode
     , granted
     , extract(epoch FROM age(clock_timestamp(), query_start)) AS duration
  FROM p
  JOIN pg_locks
 USING (pid)
  JOIN pg_stat_activity a
 USING (pid)
 UNION
SELECT -1, NULL, NULL, True, 0
 WHERE NOT EXISTS (SELECT * 
                     FROM p)
