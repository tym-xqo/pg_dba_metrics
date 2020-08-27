/* :meta
---
status: pause
threshold:
  field: blocked_locks
  gate: 5
---
*/ 
select count(distinct pid) as blocked_locks
  from pg_locks
 where not granted
;
