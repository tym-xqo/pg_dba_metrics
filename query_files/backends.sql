select count(1) as current,
  (select setting as mc from pg_settings where name = 'max_connections')::int as max_conns,
  sum(case when state = 'idle' then 1 else 0 end) as idle_conns,
  sum(case when state = 'idle in transaction' then 1 else 0 end) as xact_idle_conns,
  sum(case when state = 'active' then 1 else 0 end) as active_conns
from pg_stat_activity 
where backend_type = 'client backend'