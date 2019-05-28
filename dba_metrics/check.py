#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Collect arbitrary SQL statements from a local directory, run against one
database, and insert results to simple time series table (in the same or
separate database) with timestamp and query name columns, and a jsonb column
for the data result.

Best suited for monitoring metric-check queries that return a single row, but
in case of multiple results will insert every row of the result set, with
matching timestamp and name values

Usage:
    - As command-line script, with optional `[-j|--json]` argument will output
    one JSON object per query, otherwise will start schedule to store in target
    database
    - Invoke from other python script with `query_checks.schedule()` or
    `query_checks.get_metrics(as_json=True)`
"""
import argparse
import glob
import json
import os
from datetime import datetime

import records
from apscheduler.schedulers.blocking import BlockingScheduler
from dotenv import find_dotenv, load_dotenv
from sqlalchemy.exc import ProgrammingError

override = False
if os.getenv("METRIC_ENV", "development") == "development":
    override = True

load_dotenv(find_dotenv(), override=override)

FETCH_DB_URL = os.getenv("DATABASE_URL", "postgres://postgres@localhost/yardstick")
STORE_DB_URL = os.getenv("STORE_DB_URL", FETCH_DB_URL)

# database to measure
store_db = records.Database(STORE_DB_URL)
# database to store metrics in
fetch_db = records.Database(FETCH_DB_URL)


def get_sql(name):
    """Read sql from file matching name and return as SQL string
    """
    query_file = os.path.join("query_files", name)
    with open(query_file) as f:
        query_sql = f.read()
    return query_sql


def fetch_metric(name):
    """Submit query to the database, return results in a dict with timestamp
    and query name nodes appended
    """
    sql = get_sql(name)
    try:
        metric_result = fetch_db.query(sql)
        metric = metric_result.as_dict()
    except ProgrammingError as e:
        metric = dict(error=repr(e))
    j = {}
    j["data"] = metric
    j["stamp"] = datetime.utcnow().isoformat()
    j["name"] = name.replace(".sql", "")
    return j


def store_metric(name, as_json=False):
    """Insert metric query result in time series table in target database
    """
    metric = fetch_metric(name)
    if as_json:
        print(json.dumps(metric, default=str))
        return

    # most metric queries return a single row, but loop here so we can store
    # more than one result
    # NOTE: Also means we don't insert anything if results are empty (that's
    # good)
    for i in metric["data"]:
        stamp = metric["stamp"]
        name = metric["name"]
        payload = json.dumps(i, default=str)
        sql = (
            "insert into dba_metrics (stamp, payload, name) "
            "values (:stamp, :payload, :name)"
        )
        store_db.query(sql, stamp=stamp, payload=payload, name=name)


def get_metrics(as_json=False):
    queries = [name for name in glob.glob("query_files/*")]
    metrics = [os.path.basename(name) for name in queries]
    for name in metrics:
        store_metric(name, as_json)


def create_table():
    """Create table for storing metrics in target database if not present
    """
    sql = (
        "create table if not exists dba_metrics( "
        "stamp timestamp with time zone, "
        "payload jsonb, "
        "name text)"
    )
    store_db.query(sql)


def schedule():
    scheduler = BlockingScheduler(timezone="UTC")
    scheduler.add_job(get_metrics, "interval", seconds=10)
    print("Press Ctrl+C to exit")

    # Execution will block here until Ctrl+C is pressed.
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-j", "--json", action="store_true", default=False)
    args = parser.parse_args()
    if args.json:
        metrics = get_metrics(as_json=True)
    else:
        create_table()
        schedule()
