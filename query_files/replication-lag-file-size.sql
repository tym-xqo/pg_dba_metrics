/* :meta
---
status: clear
threshold:
  field: restart_lag
  gate: 268435456
--- */ 
with lag as (
        select slot_name
             , pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn)::BIGINT as restart_lag
             , pg_size_pretty(pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn)) as pretty_restart_lag
             , pg_wal_lsn_diff(pg_current_wal_lsn(), confirmed_flush_lsn)::BIGINT as flush_lag
          from pg_replication_slots
       ) 
select *
  from lag
 union 
 select null
     , 0
     , ''
     , 0
 where not exists (
        select *
          from lag
       )
;
