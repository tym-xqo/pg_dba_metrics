SELECT extract('epoch' FROM age(clock_timestamp(), query_start)) AS duration ,
       pid ,
       usename ,
       left(query, 80) as query
  FROM pg_stat_activity
 WHERE backend_type = 'client backend'
   AND state != 'idle'
 ORDER BY 1 DESC
 LIMIT 1;