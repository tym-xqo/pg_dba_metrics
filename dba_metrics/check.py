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
import re
from datetime import datetime

import records
import yaml
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


def get_sql(name):
    """Read sql from file matching name and return as string
    """
    query_file = os.path.join("query_files", name)
    with open(query_file) as f:
        query_sql = f.read()
    return query_sql


def get_metric(name):
    """Parse metic file and append threshold metadata
    """
    bound = re.compile(r"^\/\*---$|^---\*\/$", re.MULTILINE)
    file = f"{name}.sql"

    sql_text = get_sql(file)
    parse = bound.split(sql_text, 2)

    metric = {}
    metric["sql"] = parse[-1].strip()
    try:
        metadata = yaml.safe_load(parse[1])
        metric["threshold"] = metadata["threshold"]
        metric["status"] = metadata["status"]
    except IndexError:
        pass
    return metric


def fetch_result(metric):
    """Submit query to the database, return results in a dict with timestamp
    and query name nodes appended
    """
    sql = metric["sql"]
    try:
        result = fetch_db.query(sql)
        data = result.as_dict()
    except ProgrammingError as e:
        data = dict(error=repr(e))

    metric["data"] = data
    metric["stamp"] = utc.localize(datetime.utcnow()).isoformat()
    return metric


def print_metric(name):
    metric = get_metric(name)
    metric = fetch_result(metric)
    # TODO: better serialization default method
    print(json.dumps(metric, default=str))


def store_metric(name):
    """Insert metric query result into time series table in target database,
    Also send to alter_check unless quiet flag is set.
    """
    metric = get_metric(name)
    metric = fetch_result(metric)
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
