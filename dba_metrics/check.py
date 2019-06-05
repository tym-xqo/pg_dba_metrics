#!/usr/bin/env python
# -*- coding: future_fstrings -*-
"""Collect arbitrary SQL statements from a local directory, run against one
database. Return results as JSON. Optionally, insert results to simple time series table
(in the same or separate database) with timestamp and query name columns, and a jsonb
column for the data result.

Best suited for monitoring metric-check queries that return a single row, but in case of
multiple results will insert every row of the result set, with matching timestamp and
name values
"""
import json
import os
from datetime import datetime

import records
from dba_metrics.alert import alert_check
from dba_metrics.sql_fm import get_sql
from dotenv import find_dotenv, load_dotenv
from pytz import utc
from sqlalchemy.exc import ProgrammingError

override = False
if os.getenv("METRIC_ENV", "development") == "development":
    override = True

load_dotenv(find_dotenv(), override=override)

HOSTNAME = os.getenv("HOSTNAME", "localhost")

FETCH_DB_URL = os.getenv("DATABASE_URL", "postgres://postgres@localhost/yardstick")
STORE_DB_URL = os.getenv("STORE_DB_URL", FETCH_DB_URL)

# database to measure
fetch_db = records.Database(
    FETCH_DB_URL,
    connect_args={"application_name": "pg_dba_metrics"}
)
# database to store metrics in
store_db = records.Database(
    STORE_DB_URL,
    connect_args={"application_name": "pg_dba_metrics"}
)


def fetch_metric(name):
    """Submit query to the database, return results in a dict with timestamp
    and query name nodes appended
    """
    sql = get_sql(name)
    try:
        result = fetch_db.query(sql)
        data = result.as_dict()
    except ProgrammingError as e:
        data = dict(error=repr(e))
    j = {}
    j["data"] = data
    j["stamp"] = utc.localize(datetime.utcnow()).isoformat()
    j["name"] = name.replace(".sql", "")
    return j


# TODO: Refactor to separate methods for JSON vs Database table
def output_metric(name, as_json=True, quiet=False):
    """Insert metric query result in time series table in target database,
    or print JSON to stdout. Also send to alter_check unless quiet flag is set.
    """
    metric = fetch_metric(name)

    if not quiet:
        alert_check(metric)

    if as_json:
        # TODO: better serialization default method
        print(json.dumps(metric, default=str))
        return
    sql = (
        "insert into perf_metric (stamp, payload, name, host)"
        "values (:stamp, :payload, :name, :host)"
    )
    # Most metric queries return a single row, but loop here so we can store
    # more than one result if desired
    # NOTE: This also means we don't insert anything if results are empty
    # (that's good!)
    for i in metric["data"]:
        stamp = metric["stamp"]
        name = metric["name"]
        payload = json.dumps(i, default=str)
        store_db.query(sql, stamp=stamp, payload=payload, name=name, host=HOSTNAME)
