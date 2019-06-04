#!/usr/bin/env python
# -*- coding: future_fstrings -*--
import argparse
import glob
import os

from apscheduler.schedulers.blocking import BlockingScheduler
from dba_metrics.check import store_db, store_metric
from dotenv import find_dotenv, load_dotenv

override = False
if os.getenv("METRIC_ENV", "development") == "development":
    override = True
load_dotenv(find_dotenv(), override=override)

INTERVAL = int(os.getenv("INTERVAL", 60))


def get_metrics(as_json=True, quiet=False):
    """Loop through all the queries in query_files directory,
    and submit for handling
    """
    queries = [name for name in glob.glob("query_files/*")]
    metrics = [os.path.basename(name) for name in queries]
    for name in metrics:
        store_metric(name, as_json, quiet)


def create_table():
    """Create table for storing metrics in target database if not present
    """
    sql = (
        "create table if not exists perf_metric( "
        "metric_id bigserial primary key, "
        "stamp timestamp with time zone, "
        "payload jsonb, "
        "name text, "
        "host text)"
    )
    store_db.query(sql)


def schedule(as_json=False, quiet=False):
    """Schedule get_metrics job in APScheduler, set to run at configured $INTERVAL
    """
    scheduler = BlockingScheduler(timezone="UTC")
    scheduler.add_job(get_metrics, "interval", [as_json, quiet], seconds=INTERVAL)
    print("Press Ctrl+C to exit")

    # Execution will block here until Ctrl+C is pressed.
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass


def main():
    """Handle arguments and handoff to appropriate methods
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-1", "--single")
    parser.add_argument("-s", "--schedule", action="store_true", default=False)
    parser.add_argument("-q", "--no-alerts", action="store_true", default=False)
    args = parser.parse_args()
    if args.single:
        name = f"{args.single}.sql"
        store_metric(name=name, as_json=True, quiet=args.no_alerts)
    elif args.schedule:
        create_table()
        schedule(as_json=False, quiet=args.no_alerts)
    else:
        get_metrics(as_json=True, quiet=args.no_alerts)


if __name__ == "__main__":
    main()
