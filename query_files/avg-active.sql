with h as (select extract(epoch from age(clock_timestamp(), query_start)) as duration 
            from pg_stat_activity 
           where backend_type = 'client backend' 
             and state != 'idle' 
             and application_name != 'pg_dba_metrics')
select avg(duration) as avg_duration from h;
