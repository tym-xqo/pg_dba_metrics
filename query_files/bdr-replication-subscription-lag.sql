/* :meta
---
status: clear
threshold:
  field: replication_replay_lag
  gate: 30
---
*/ 
select node_group_name 
     , origin_name 
     , sub_enabled 
     , sub_slot_name 
     , subscription_status 
     , extract(epoch from age(now(), last_xact_replay_timestamp)) as time_lag
  from bdr.subscription_summary;
