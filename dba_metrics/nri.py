import json

from dba_metrics.__main__ import all_metrics, get_metric
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(), override=True)

JSON_HEADER = """
{
  "name": "com.benchprep.test-integration",
  "protocol_version": "3",
  "integration_version": "0.0.1",
  "data": [
    {
      "entity": {
        "name": "postgres-custom",
        "type": "database-metric",
        "id_attributes": [
          {
            "key": "environment",
            "value": "development"
          }
        ]
      },
      "metrics": [{}],
      "inventory": {},
      "events": [],
      "add_hostname": true
    }
  ]
}
"""

JSON_BLOCK = """
{
  "name": "com.benchprep.test-integration",
  "protocol_version": "3",
  "integration_version": "0.0.1",
  "data": [{
    "entity": {
      "name": "postgres-custom",
      "type": "database-metric",
      "id_attributes": [{
        "key": "environment",
        "value": "development"
      }]
    },
    "metrics": [{
      "displayName": "postgres-custom",
      "entityName": "database-metric:postgres-custom",
      "event_type": "BenchPrepTestEvent",
      "bppg.avg-active.avg_duration": 0.001298,
      "bppg.locks.lock_count": 1
    }],
    "inventory": {},
    "events": [],
    "add_hostname": true
  }]
}
"""


def setup_header():
    payload = json.loads(JSON_HEADER)
    return payload


def sample_metrics():
    metrics = dict(
        displayName="test_entity",
        entityName="meaningless_number:test_entity",
        event_type="BenchPrepTestEvent",
    )
    for metric in all_metrics():
        metric = get_metric(metric)
        if metric.error:
            continue
        data = metric.result
        check = metric.metadata["threshold"]["field"]
        value = max([row[check] for row in data])
        metric_key = ".".join(["bppg", metric.name, check])
        metrics[metric_key] = value
    metrics = [metrics]
    return metrics


def main():
    # header = setup_header()
    # metrics = sample_metrics()
    # header["data"][0]["metrics"] = metrics
    # payload = json.dumps(header)
    # print(payload)
    block = json.loads(JSON_BLOCK)
    payload = json.dumps(block)
    print(payload)


if __name__ == "__main__":
    main()
