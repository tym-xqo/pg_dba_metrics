---
status: clear
threshold:
  field: duration
  gate: 300
---
with submsg as (
SELECT EXTRACT(EPOCH FROM AGE(NOW(), last_msg_receipt_time)) AS duration
FROM pg_stat_subscription)
SELECT * FROM submsg
UNION
SELECT 0
WHERE NOT EXISTS (SELECT * FROM submsg)
;