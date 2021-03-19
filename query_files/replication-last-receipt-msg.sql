/* 
---
threshold:
  field: duration
  gate: 300
---
*/ 
with submsg as (
        select subname as subscription_name
             , EXTRACT(EPOCH from AGE(NOW(), last_msg_receipt_time)) as duration
          from pg_stat_subscription
       ) select *
  from submsg
 union 
select null
     , 0
 where not exists (
        select *
          from submsg
       ) 
;
