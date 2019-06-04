#!/usr/bin/env python
# -*- coding: future_fstrings -*--
import os
from itertools import cycle

import yaml
from dotenv import find_dotenv, load_dotenv
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


def update_config(metric):
    """Rewrite config with new status after change
    """
    with open("config.yaml", "r") as config_file:
        config = yaml.safe_load(config_file.read())
    name = metric["name"]
    config_match = list(filter(lambda m: m["name"] != name, config))
    metric_config = {
        key: metric[key] for key in ("name", "check", "threshold", "status")
    }
    config_match.append(metric_config)
    with open("config.yaml", "w") as config_file:
        config_file.write(yaml.safe_dump(config_match))


def swap_status(status):
    """Toggle status between "clear" and "failure" on check status change
    """
    opts = cycle(["clear", "failure"])
    new_status = next(opts)
    if status == new_status:
        new_status = next(opts)
    return new_status


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
    """Test whether metric name is found in threshold config, and
    append config settings to metric results if so, then
    pass to alerting methods
    """
    with open("config.yaml", "r") as config_file:
        config = yaml.safe_load(config_file.read())
    name = metric["name"]
    if any(m["name"] == name for m in config):
        config_match = list(filter(lambda m: m["name"] == name, config))[0]
        metric = dict(config_match, **metric)
        alert = check_metric(metric)
        return alert
    else:
        pass


if __name__ == "__main__":
    metric = {"data": [{"test_data_point": -1}], "name": "test_metric"}
    alert_check(metric)
