import json


def nri_output():
    with open("metric.json", "r") as jsonfile:
        payload = jsonfile.read()
        payload = json.loads(payload)
    return json.dumps(payload)


if __name__ == "__main__":
    output = nri_output()
    print(output)
