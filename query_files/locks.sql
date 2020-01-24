/* :meta
---
status: pause
threshold:
  field: lock_count
  gate: 1000
---
*/
SELECT count(*) AS lock_count
     , mode
     , granted
  FROM pg_locks
 GROUP BY 2,
          3;
