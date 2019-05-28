SELECT count(1) AS blocked_locks
  FROM pg_locks
 WHERE NOT GRANTED