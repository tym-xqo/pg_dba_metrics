/* 
---
threshold:
  field: lock_count
  gate: 1000
---
*/ 
select count(*) as lock_count 
     , mode 
     , granted
  from pg_locks
 group by 2
        , 3
;
