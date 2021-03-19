/* 
---
threshold:
  field: error_count
  gate: 1
--- */
select sum(case when status = 'OK' then 0 else 1 end) as error_count
  from bdr.monitor_group_raft();
