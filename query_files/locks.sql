select count(*) as locks
     , mode
     , granted 
  from pg_locks 
 group by 2,3;