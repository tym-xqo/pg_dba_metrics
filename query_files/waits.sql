/* 
---
threshold:
  field: duration
  gate: 3600
--- */
with w AS(
        select extract(epoch from max(age(clock_timestamp(), query_start))) as duration
             , wait_event_type
             , pid
          from pg_stat_activity
         where backend_type = 'client backend'
           and wait_event_type is not null
           and query_start is not null
           and state != 'idle'
           and application_name != 'pg_dba_metrics'
         group by 2
                , 3
         order by 1 desc
         limit 1
       )
select *
  from w
 union
select 0
     , 'none'
     , -1
 where not exists (
        select *
          from w
       )
;
