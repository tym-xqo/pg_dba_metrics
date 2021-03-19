/* 
---
threshold:
  field: duration
  gate: 1800
--- */
with d as (
        select extract(epoch from age(clock_timestamp(), query_start)) as duration
             , pid
             , usename
             , application_name
             , state
             , left(query, 80) as query
          from pg_stat_activity
         where backend_type = 'client backend'
           and state != 'idle'
           and application_name != 'pg_dba_metrics'
           and application_name != 'postgres_fdw'
         order by 1 desc
         limit 1
       )
select *
  from d
 union
select 0
     , -1
     , null
     , null
     , 'idle'
     , ''
 where not exists (
        select *
          from d
       )
;
