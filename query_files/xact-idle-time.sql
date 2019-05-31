SELECT pid
     , usename
     , left(query, 80) AS query
     , extract(epoch FROM age(clock_timestamp(), query_start)) AS duration
 FROM pg_stat_activity
WHERE backend_type = 'client backend'
  AND state = 'idle in transaction'
ORDER BY 4 desc
LIMIT 1; 
