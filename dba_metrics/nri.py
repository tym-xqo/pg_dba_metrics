import json


def nri_output():
    with open("metric.json", "r") as jsonfile:
        payload = jsonfile.read()
        payload = json.loads(payload)
    return json.dumps(payload)
