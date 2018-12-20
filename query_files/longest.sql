select extract('epoch' from age(now(), query_start)) as duration
     , pid
     , usename
     , query 
  from pg_stat_activity
 where backend_type = 'client backend' 
   and state != 'idle' 
 order by 1 desc 
 limit 1;