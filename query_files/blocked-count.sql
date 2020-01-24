/* :meta
---
status: pause
threshold:
  field: blocked_locks
  gate: 5
---
*/
SELECT count(DISTINCT pid) AS blocked_locks
  FROM pg_locks
 WHERE NOT GRANTED
