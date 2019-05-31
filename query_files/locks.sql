SELECT count(*) AS locks,
       mode,
       granted
  FROM pg_locks
 GROUP BY 2,
          3;