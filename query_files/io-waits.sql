SELECT count(*)
  FROM pg_stat_activity
 WHERE wait_event_type = 'IO';