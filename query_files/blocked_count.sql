select count(1) as blocked_locks
  from pg_locks
 where not granted