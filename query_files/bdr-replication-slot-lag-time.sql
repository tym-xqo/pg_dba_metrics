/* 
---
threshold:
  field: replay_lag_seconds
  gate: 300
--- */
select slot_name
     , extract('epoch' from replay_lag)::int as replay_lag_seconds
     , replay_lag_bytes::bigint
     , replay_lag_size
  from bdr.node_slots
 where slot_name not like 'bdr_wmx_rail%_wmx_api'
