---
status: clear
threshold:
  field: duration
  gate: 300
---
SELECT EXTRACT(EPOCH FROM AGE(NOW(), last_msg_receipt_time)) AS duration
FROM pg_stat_subscription;
