SELECT count(DISTINCT pid) AS blocked_locks
  FROM pg_locks
 WHERE NOT GRANTED