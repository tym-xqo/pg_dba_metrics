SELECT count(*) as io_wait_count
  FROM pg_stat_activity
 WHERE wait_event_type = 'IO';
 