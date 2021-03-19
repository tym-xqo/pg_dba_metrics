# pg_dba_metrics

Simple python script that executes arbitrary queries against a database, and returns results as JSON formatted for consumption by New Relic custom metrics API
## Usage

### Installation

``` bash
git clone https://github.com/tym-xqo/pg_dba_metrics
cd pg_dba_metrics
pip install -r requirements.txt
pip install .
```

### Configuration

#### Script config

For manual execution of the script, set `DATABASE_URL` in the environment for connection to the database to be monitored. See `.env.example` for an example. Generally, the intended usage is for New Relic's Infrastructure agent to run the script; see `nri-custom-pg.yml` for an example YAML config to set that integration up.

#### Check and thresholds config

Metric checks are added by creating plain SQL files in local `query_files` directory. The `nri_metrics.py` script will search this directory in the working directory from which it is run. Generally, these are expected to be queries against [database stats tables](https://www.postgresql.org/docs/current/monitoring-stats.html) which return a single numeric value. (It is possible, however, for these queries to run any arbitrary SQL the operator may be interested in checking periodically.)

Thresholds for checks are set in a YAML front matter block before the query SQL, set off by `---` delimiters. The format is a status and a threshold definition, like so:

``` yaml
---
threshold:
  field: <column name to find value in query result>
  gate: <a number at which alert will fire>
---
# SELECT ...

```
