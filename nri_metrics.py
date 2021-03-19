import json
import os
import re
from pathlib import Path

import inflection
import yaml
from raw.db import result_from_file

JSON_HEADER = """
{
  "name": "com.benchprep.custom_pg",
  "protocol_version": "3",
  "integration_version": "0.1.0",
  "data": [
    {
      "entity": {
        "name": "customPostgres",
        "type": "db",
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


def setup_header():
    payload = json.loads(JSON_HEADER)
    return payload


def all_metrics():
    metrics = list(Path(os.getenv("QUERY_PATH", "query_files")).glob("**/*"))
    # metric_names = [metric.stem for metric in metrics]
    return metrics


def extract_metadata(path):
    """Find frontmatter comment in query file and load yaml from it if present"""
    with open(path) as query_file:
        query_string = query_file.read()
    metadata = {}
    meta_comment = re.search(r"---[\s\S]+?---", query_string, re.MULTILINE)
    if meta_comment:
        meta_string = meta_comment[0].strip("---")
        metadata = yaml.safe_load(meta_string)

    return metadata


def sample_metrics():
    metrics = dict(
        displayName="customPostgres",
        entityName="db:customPostgres",
        event_type="BenchPrepCustomPostgresEvent",
    )
    for metric in all_metrics():
        result = result_from_file(metric)
        metadata = extract_metadata(metric)
        check = metadata["threshold"]["field"]
        value = max([row[check] for row in result])
        check = inflection.camelize(check.replace("-", "_"))
        check = check[0].lower() + check[1:]
        name = inflection.camelize(metric.stem.replace("-", "_"))
        name = name[0].lower() + name[1:]
        metric_key = ".".join(["pg", name, check])
        metrics[metric_key] = value
    metrics = [metrics]
    return metrics


def main():
    header = setup_header()
    metrics = sample_metrics()
    header["data"][0]["metrics"] = metrics
    payload = json.dumps(header, default=str)
    print(payload)


if __name__ == "__main__":
    main()
