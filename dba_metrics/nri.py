import json

from dba_metrics.__main__ import all_metrics, get_metric

JSON_HEADER = """
{
  "name": "com.benchprep.test-integration",
  "protocol_version": "3",
  "integration_version": "0.0.1",
  "data": [
    {
      "entity": {
        "name": "test_entity",
        "type": "meaningless_number",
        "id_attributes": [
          {
            "key": "environment",
            "value": "development"
          }
        ]
      },
      "metrics": [{}],
      "inventory": {},
      "events": []
    }
  ]
}
"""


def setup_header():
    payload = json.loads(JSON_HEADER)
    return payload


def sample_metrics():
    metrics = dict(
        displayName="test_entity",
        entityName="meaningless_number:test_entity",
        event_type="TestEvent",
    )
    for metric in all_metrics():
        metric = get_metric(metric)
        if metric.error:
            continue
        data = metric.result
        check = metric.metadata["threshold"]["field"]
        value = max([row[check] for row in data])
        metric_key = ".".join([metric.name, check])
        metrics[metric_key] = value
    metrics = [metrics]
    return metrics


def main():
    header = setup_header()
    metrics = sample_metrics()
    header["metrics"] = metrics
    payload = json.dumps(header)
    print(payload)


if __name__ == "__main__":
    main()
