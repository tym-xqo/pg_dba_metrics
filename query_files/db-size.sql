/* :meta
---
status: clear
threshold:
  field: db_size
  gate: 900
--- */
select pg_database_size(datname)/1073741824::float db_size
     , pg_size_pretty(pg_database_size(datname)) db_size_pretty
  from pg_database
 where datname = 'wmx_rails_api_production';

