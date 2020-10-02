/* :meta
---
status: clear
threshold:
  field: duration
  gate: 720
--- */
with i as (
        select pid
             , usename
             , left(query, 80) as query
             , extract(epoch from age(clock_timestamp(), xact_start)) as duration
          from pg_stat_activity
         where backend_type = 'client backend'
           and state = 'idle in transaction'
           and application_name != 'postgres_fdw'
         order by 4 desc
         limit 1
       )
select *
  from i
 union
select 0
     , 'no user'
     , 'no query'
     , 0
 where not exists (
        select *
          from i
       )
;
