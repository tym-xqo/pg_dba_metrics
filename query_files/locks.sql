SELECT count(*) AS lock_count
     , mode
     , granted
  FROM pg_locks
 GROUP BY 2,
          3;