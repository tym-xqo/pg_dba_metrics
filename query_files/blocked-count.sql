---
status: failure
threshold:
  field: blocked_locks
  gate: 1
---
SELECT count(DISTINCT pid) AS blocked_locks
  FROM pg_locks
 WHERE NOT GRANTED
