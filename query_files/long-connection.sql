/* :meta
---
status: clear
threshold:
  field: duration
  gate: 3600
--- */ 
with c as (
        select extract(epoch from age(clock_timestamp(), query_start)) as duration 
             , pid 
             , usename 
             , application_name 
             , state 
             , left(query, 80) as query
          from pg_stat_activity
         where backend_type = 'client backend'
           and query_start is not null
           and application_name != 'pg_dba_metrics'
         order by 1 desc
         limit 1
       ) 
select *
  from c
 union 
select 0
     , -1
     , null
     , null
     , 'idle'
     , ''
 where not exists (
        select *
          from c
        )
;
