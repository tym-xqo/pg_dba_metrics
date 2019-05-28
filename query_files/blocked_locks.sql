SELECT pid ,
       locktype ,
       mode ,
       granted
  FROM pg_locks
 WHERE NOT granted;