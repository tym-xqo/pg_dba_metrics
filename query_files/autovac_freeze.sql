SELECT max_age, 
       transactions, 
       ROUND(100*(transactions/max_age::float)) AS percent 
 FROM (SELECT foo.max_age::int
            , age(datfrozenxid) AS transactions
            , datname
         FROM pg_database d 
         JOIN (SELECT setting AS max_age 
                 FROM pg_settings 
                WHERE name = 'autovacuum_freeze_max_age') AS foo
           ON (true) 
        WHERE d.datallowconn
        and datname = current_database()) AS foo2 