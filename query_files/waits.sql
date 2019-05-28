SELECT max(age(clock_timestamp(), query_start)) AS longest ,
       count(*) AS wait_count ,
       wait_event_type ,
       pid
  FROM pg_stat_activity
 WHERE backend_type = 'client backend'
   AND wait_event_type IS NOT NULL
   AND query_start IS NOT NULL --  and state != 'idle'

 GROUP BY 3,
          4
 ORDER BY 1 DESC
 LIMIT 1
 ;