/* :meta
---
status: clear
threshold:
  field: restart_lag
  gate: 268435456
---
*/
with lag as (
SELECT
  slot_name,
  pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn)::INTEGER AS restart_lag,
  pg_size_pretty(pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn)) as pretty_restart_lag,
  pg_wal_lsn_diff(pg_current_wal_lsn(), confirmed_flush_lsn)::INTEGER AS flush_lag
FROM pg_replication_slots
--WHERE slot_name != 'reporting_subscription'
)
SELECT * FROM lag
UNION
SELECT NULL, 0, '', 0 
WHERE NOT EXISTS (SELECT * FROM lag)
;
