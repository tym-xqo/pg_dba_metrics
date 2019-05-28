<<<<<<< HEAD
SELECT extract('epoch' FROM age(clock_timestamp(), query_start)) AS duration ,
       pid ,
       usename ,
       left(query, 80) as query
  FROM pg_stat_activity
 WHERE backend_type = 'client backend'
   AND state != 'idle'
 ORDER BY 1 DESC
 LIMIT 1;
=======
select extract(epoch from age(clock_timestamp(), query_start)) as duration
     , pid
     , usename
     , application_name
     , left(query, 80) as query
  from pg_stat_activity
 where backend_type = 'client backend' 
   and state != 'idle' 
 order by 1 desc 
 limit 1;
>>>>>>> mnene-alerting
