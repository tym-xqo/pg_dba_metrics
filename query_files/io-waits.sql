/* 
---
threshold:
  field: io_wait_count
  gate: 25
--- */ 
select count(*) as io_wait_count
  from pg_stat_activity
 where wait_event_type = 'IO';
