select extract(epoch from age(clock_timestamp(), query_start)) as duration
     , pid
     , usename
     , application_name
     , state
     , left(query, 80) as query
  from pg_stat_activity
 where backend_type = 'client backend' 
  --  and state != 'idle' 
 order by 1 desc 
 limit 1;
