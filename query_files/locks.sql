/*---
check: lock_count
name: locks
status: clear
threshold: 1000
---*/
SELECT count(*) AS lock_count
     , mode
     , granted
  FROM pg_locks
 GROUP BY 2,
          3;