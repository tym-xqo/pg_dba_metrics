#!/usr/bin/env python
# -*- coding: utf-8 -*
import os
from argparse import ArgumentParser
from pprint import pprint

import slack

client = slack.WebClient(token=os.getenv("SLACK_TOKEN"))


def slack_post(message="Hello, world!"):
    response = client.chat_postMessage(
        channel="UDQ1P3A1E",
        blocks=[{"type": "section", "text": {"type": "mrkdwn", "text": message}}],
    )
    return response


if __name__ == "__main__":
    parse = ArgumentParser()
    parse.add_argument("message", nargs="?", default="Hello, world!")
    args = parse.parse_args()
    r = slack_post(args.message)
    pprint(r.data)
