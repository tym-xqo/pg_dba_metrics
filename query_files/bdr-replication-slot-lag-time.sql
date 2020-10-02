/* :meta
---
status: clear
threshold:
  field: replay_lag_seconds
  gate: 300
--- */
select slot_name
     , extract('epoch' from replay_lag)::int as replay_lag_seconds
     , replay_lag_bytes::int
     , replay_lag_size
  from bdr.node_slots
 where slot_name != 'bdr_wmx_rail9f667b5_wmx_api'
