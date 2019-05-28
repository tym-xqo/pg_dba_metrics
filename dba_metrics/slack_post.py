import os

import slack
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

TOKEN = os.getenv("SLACK_TOKEN")
CHANNEL = os.getenv("CHANNEL")

client = slack.WebClient(TOKEN)


def slack_post(message="Hello world!"):
    r = client.chat_postMessage(channel=CHANNEL, text=message)
    return r


if __name__ == "__main__":
    slack_post("Something blah blah")
