/* :meta
---
status: clear
threshold:
  field: error_count
  gate: 1
--- */
with e as (
select (select count(*) from bdr.worker_errors) as error_count
     , worker_pid
     , error_time
     , error_message
  from  bdr.worker_errors)
select *
  from e
 union
select 0
     , -1
     , '1970-01-01T00:00:00'
     , ''
 where not exists (select * from e)
;
