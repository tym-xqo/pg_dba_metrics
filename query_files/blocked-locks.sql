/* 
---
threshold:
  field: duration
  gate: 300
--- */ 
with p as (
        select distinct pid
          from pg_locks
         where not granted
       ) 
select pid 
     , pg_blocking_pids(pid) 
     , mode 
     , granted 
     , extract(epoch from age(clock_timestamp(), query_start)) as duration
  from p
  join pg_locks using (pid)
  join pg_stat_activity a using (pid)
 union 
 select -1
     , null
     , null
     , true
     , 0
 where not exists (
        select *
          from p
       )
;
