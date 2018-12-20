select sum(xact_commit) as commits
     , sum(xact_rollback) as rollbacks
     , sum(xact_commit + xact_rollback) as total_transactions
     , min(stats_reset) as reset 
  from pg_stat_database;
