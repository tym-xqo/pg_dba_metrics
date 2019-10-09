---
status: clear
threshold:
  field: restart_lag
  gate: 33554432
---
SELECT
  pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn)::INTEGER AS restart_lag,
  pg_wal_lsn_diff(pg_current_wal_lsn(), confirmed_flush_lsn)::INTEGER AS flush_lag
FROM pg_replication_slots
WHERE slot_name = 'session_database_replication_slot';
