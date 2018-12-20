select max(age(now(), query_start)) as longest
     , count(*) as wait_count
     , wait_event_type 
  from pg_stat_activity 
 where backend_type = 'client backend'
   and wait_event_type is not null 
  --  and query_start is not null 
  --  and state != 'idle' 
   
 group by 3 order by 1 desc;