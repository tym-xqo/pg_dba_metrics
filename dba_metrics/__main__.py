import argparse
import json
import os

import records
from apscheduler.schedulers.blocking import BlockingScheduler
from dotenv import find_dotenv, load_dotenv
from nerium.query import get_result_set
from nerium.formatter import get_format
from .alert import alert_check
from pathlib import Path

override = False
if os.getenv("METRIC_ENV", "development") == "development":
    override = True

load_dotenv(find_dotenv(), override=override)

HOSTNAME = os.getenv("HOSTNAME", "localhost")
INTERVAL = int(os.getenv("INTERVAL", 60))
DATABASE_URL = os.getenv("DATABASE_URL", "postgres://postgres@localhost/yardstick")
STORE_DB_URL = os.getenv("STORE_DB_URL", DATABASE_URL)


def get_metric(name, quiet=False):
    metric = get_result_set(name)
    metric.executed += "Z"
    alert_check(metric)
    return metric


def print_metric(name):
    metric = get_metric(name)
    format = get_format("print")
    formatted = json.dumps(format.dump(metric).data)
    return formatted


def store_metric(name):
    # database to store metrics in
    store_db = records.Database(
        STORE_DB_URL, connect_args={"application_name": "pg_dba_metrics"}
    )
    metric = get_metric(name)
    sql = (
        "insert into perf_metric (stamp, payload, name, host) "
        "values (:stamp, :payload, :name, :host) "
        "returning metric_id"
    )
    for i in metric.result:
        stamp = metric.executed
        payload = json.dumps(i, default=str)
        insert = store_db.query(
            sql, stamp=stamp, payload=payload, name=name, host=HOSTNAME
        )
        return insert.export("json")


def all_metrics():
    metrics = list(Path(os.getenv("QUERY_PATH", "query_files")).glob("**/*"))
    metric_names = [metric.stem for metric in metrics]
    return metric_names


def output_all(output_function):
    metrics = all_metrics()
    for name in metrics:
        output = output_function(name)
        yield output


def schedule(scheduled_function, *args):
    """Schedule get_metrics job in APScheduler, set to run at configured $INTERVAL
    """
    scheduler = BlockingScheduler(timezone="UTC")
    scheduler.add_job(scheduled_function, "interval", [args], seconds=INTERVAL)
    print("Press Ctrl+C to exit")

    # Execution will block here until Ctrl+C is pressed.
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name")
    parser.add_argument("-s", "--store", action="store_true", default=False)
    parser.add_argument("-S", "--schedule", action="store_true", default=False)
    args = parser.parse_args()
    quiet = args.no_alerts
    output_function = print_metric
    if args.store:
        output_function = store_metric
    if args.schedule:
        o = schedule(output_function)
    o = output_all(print_metric)
    for i in o:
        print(i)
