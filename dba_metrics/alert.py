#!/usr/bin/env python
# -*- coding: future_fstrings -*--
import os
from itertools import cycle

import yaml
from dotenv import find_dotenv, load_dotenv
from dba_metrics.check import fetch_metric
from dba_metrics.slack_post import slack_post

override = False
if os.getenv("METRIC_ENV", "development") == "development":
    override = True

load_dotenv(find_dotenv(), override=override)

HOSTNAME = os.getenv("HOSTNAME", "localhost")


def send_alert(metric):
    """Post a message to Slack when a metric check fails or clears.
    """
    name = metric["name"]
    check = metric["check"]
    threshold = metric["threshold"]
    status = metric["status"]
    value = metric["value"]
    full_metric = yaml.safe_dump(metric)

    title = f"{HOSTNAME} {status}"

    message = (
        f"Metric *{name}* {check} is {value}\nThreshold is {threshold}\n"
        f"```{full_metric}```"
    )

    color = "good"
    if status == "failure":
        color = "danger"

    alert = slack_post(title=title, message=message, color=color)
    return alert


def swap_status(status):
    """Toggle status between "clear" and "failure" on check status change
    """
    opts = cycle(["clear", "failure"])
    new_status = next(opts)
    if status == new_status:
        new_status = next(opts)
    return new_status


def update_config(metric):
    """Rewrite sql metadata with new status after change
    """
    sql = metric["sql"]
    metadata = {
        key: metric[key] for key in ("check", "threshold", "status")
    }
    metadata_yaml = yaml.safe_dump(metadata)
    metadata_block = f"/*---\n{metadata_yaml}---*/"
    query_file = os.path.join("query_files", f"{metric['name']}.sql")
    with open(query_file, "w") as config_file:
        new_content = "\n".join([metadata_block, sql])
        config_file.write(new_content)


def check_metric(metric):
    """Compare metric check value against threshold;
    Update status and send alert if comparsison triggers status change
    """
    # TODO: Support failure modes other than `> threshold`
    data = metric["data"]
    status = metric["status"]
    check = metric["check"]
    threshold = metric["threshold"]
    alert = None

    if data:
        value = max([row[check] for row in data])
        metric["value"] = value

        test = value >= threshold
        if status == "failure":
            test = value < threshold
        if test:
            metric["status"] = swap_status(status)
            alert = send_alert(metric)
            update_config(metric)

    return alert


def alert_check(metric):
    """If metric has threshold front matter, append metadata
    to metric results and pass to alerting methods
    """
    metadata = parse_frontmatter(metric)
    if metadata:
        metric = dict(metric, **metadata)
        alert = check_metric(metric)
        return alert
    else:
        # no-op if metric doesn't have threshold metadata
        pass


if __name__ == "__main__":
    alert_check("test.sql")
