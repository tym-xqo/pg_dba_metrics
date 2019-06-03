#!/usr/bin/env python
# -*- coding: future_fstrings -*--
import os
from itertools import cycle

import yaml
from dotenv import find_dotenv, load_dotenv
from slack_post import slack_post

override = False
if os.getenv("METRIC_ENV", "development") == "development":
    override = True

load_dotenv(find_dotenv(), override=override)

HOSTNAME = os.getenv("HOSTNAME", "localhost")

CONFIG = yaml.safe_load(open("config.yaml", "r"))


def send_alert(metric, value):
    # TODO: include raw metric JSON as attachment
    name = metric["name"]
    check = metric["check"]
    threshold = metric["threshold"]
    status = metric["status"]
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
    name = metric["name"]
    config_match = list(filter(lambda m: m["name"] != name, CONFIG))
    metric_config = {
        key: metric[key] for key in ("name", "check", "threshold", "status")
    }
    config_match.append(metric_config)
    with open("config.yaml", "w") as config_file:
        config_file.write(yaml.safe_dump(config_match))


def swap_status(status):
    opts = cycle(["clear", "failure"])
    new_status = next(opts)
    if status == new_status:
        new_status = next(opts)
    return new_status


def check_metric(metric):
    # TODO: Support failure modes other than `> threshold`
    data = metric["data"]
    status = metric["status"]
    check = metric["check"]
    threshold = metric["threshold"]
    alert = None

    for row in data:
        value = row[check]
        test = value >= threshold
        if status == "failure":
            test = value < threshold
        if test:
            metric["status"] = swap_status(status)
            alert = send_alert(metric, value)
            update_config(metric)
    return alert


def alert_check(metric):
    name = metric["name"]
    if any(m["name"] == name for m in CONFIG):
        config_match = list(filter(lambda m: m["name"] == name, CONFIG))[0]
        metric = dict(config_match, **metric)
        alert = check_metric(metric)
        return alert
    else:
        pass


if __name__ == "__main__":
    metric = {"data": [{"test_data_point": -1}], "name": "test_metric"}
    alert_check(metric)
