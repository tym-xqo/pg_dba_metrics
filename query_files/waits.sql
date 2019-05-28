
SELECT extract(epoch FROM max(age(clock_timestamp(), query_start))) AS longest ,
      --  count(*) AS wait_count ,
       wait_event_type,
       pid
  FROM pg_stat_activity
 WHERE backend_type = 'client backend'
   AND state IN ('active', 'idle in transaction')
   AND wait_event_type IS NOT NULL
  --  AND wait_event_type != 'Client'
   AND query_start IS NOT NULL
 --  and query_start is not null
  -- and state != 'idle'

 GROUP BY 2, 3
 ORDER BY 1 DESC
 LIMIT 1;
