  WITH P AS (
       SELECT DISTINCT pid 
         FROM pg_locks 
        WHERE NOT granted)
SELECT pid
     , pg_blocking_pids(pid)
     , mode
     , granted
     , age(clock_timestamp(), a.query_start) as duration
  FROM P
  JOIN pg_locks
 USING (pid)
  JOIN pg_stat_activity a
 USING (pid);