  WITH P AS (
       SELECT DISTINCT pid 
         FROM pg_locks 
        WHERE NOT granted)
SELECT pid
     , pg_blocking_pids(pid)
     , mode
     , granted
     , extract(epoch FROM age(clock_timestamp(), query_start)) AS duration
  FROM P
  JOIN pg_locks
 USING (pid)
  JOIN pg_stat_activity a
 USING (pid);