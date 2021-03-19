/* 
---
threshold:
  field: avg_duration
  gate: 30
---
*/ 
with h as (
        select extract(epoch from age(clock_timestamp(), query_start)) as duration
          from pg_stat_activity
         where backend_type = 'client backend'
           and state != 'idle'
           and application_name != 'pg_dba_metrics'
       ) 
select coalesce(avg(duration), 0) as avg_duration
  from h;
