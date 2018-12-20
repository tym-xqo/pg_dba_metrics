select pid
     , locktype
     , mode
     , granted 
  from pg_locks 
 where not granted;