#!/usr/bin/env python
# -*- coding: utf-8 -
from slack_post import slack_post


def send_alert(name, data_point, value, threshold):
    message_template = (
        f"Metric *{name}* {data_point} is {value}\nThreshold is {threshold}"
    )
    post_ = slack_post(message=message_template)
    return post_


def parse_metric(metric={}, data_point="test_data_point", threshold=0):
    if not metric:
        metric = {"data": [{"test_data_point": 1}], "name": "test_metric"}
    data = metric["data"]
    name = metric["name"]
    for row in data:
        try:
            if row[data_point] > threshold:
                alert = send_alert(name, data_point, row[data_point], threshold)
        except KeyError as e:
            value = repr(e).split("\n")[-1]
            alert = send_alert(name, data_point, value, threshold)
    return alert


if __name__ == "__main__":
    parse_metric()
