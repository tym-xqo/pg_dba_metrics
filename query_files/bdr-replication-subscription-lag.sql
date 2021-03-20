/* 
---
threshold:
  field: time_lag
  gate: 300
---
*/ 
with s as (
select node_group_name 
     , origin_name 
     , sub_enabled 
     , sub_slot_name 
     , subscription_status 
     , extract(epoch from age(now(), last_xact_replay_timestamp)) as time_lag
  from bdr.subscription_summary
)
select * from s
union
select 'wmx_rails_api'
     , 'na'
     , false
     , 'na'
     , 'na'
     , 0
 where not exists (select * from s); 
