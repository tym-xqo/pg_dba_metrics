/* 
---
threshold:
  field: duration
  gate: 60
--- */
with i as (
        select pid
             , usename
             , left(query, 80) as query
             , extract(epoch from age(clock_timestamp(), state_change)) as duration
          from pg_stat_activity
         where backend_type = 'client backend'
           and state = 'idle in transaction'
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
     , 'none'
 where not exists (
        select *
          from i
       )
;
