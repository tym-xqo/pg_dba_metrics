/* 
---
threshold:
  field: error_count
  gate: 1
--- */
with e as (
select (select count(*) from bdr.worker_errors) as error_count
     , worker_pid
     , error_time
     , error_message
  from  bdr.worker_errors
  where error_time > '2020-11-06')
select *
  from e
 union
select 0
     , -1
     , '9999-12-31T11:59:59'
     , ''
 where not exists (select * from e)
;
