/* :meta
---
status: clear
threshold:
  field: duration
  gate: 60
--- */
WITH i AS (
SELECT pid
     , usename
     , left(query, 80) AS query
     , extract(epoch FROM age(clock_timestamp(), query_start)) AS duration
     , query AS full_query
 FROM pg_stat_activity
WHERE backend_type = 'client backend'
  AND state = 'idle in transaction'
ORDER BY 4 desc
LIMIT 1)
SELECT * FROM i
UNION
SELECT 0, 'no user', 'no query', 0, 'none'
 WHERE NOT EXISTS (SELECT * FROM i)
