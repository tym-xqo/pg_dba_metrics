select pid
     , usename
     , query
     , extract('epoch' from age(now(), query_start)) as duration
 from pg_stat_activity 
where backend_type = 'client backend' 
  and state = 'idle in transaction' 
 