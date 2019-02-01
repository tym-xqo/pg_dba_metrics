select true::bool as connected, extract('epoch' from (now() - pg_postmaster_start_time())) as uptime
