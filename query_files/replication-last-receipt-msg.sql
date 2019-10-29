---
status: clear
threshold:
  field: duration
  gate: 300
---
with submsg as (
SELECT 
subname as subscription_name,
EXTRACT(EPOCH FROM AGE(NOW(), last_msg_receipt_time)) AS duration
FROM pg_stat_subscription)
SELECT * FROM submsg
UNION
SELECT NULL, 0
WHERE NOT EXISTS (SELECT * FROM submsg)
;
