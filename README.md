# pg_dba_metrics

Simple python app that executes arbitrary queries against a database, and returns results as timestamped JSON suitable for insertion to a time series table, and checking results against configurable thresholds for alerting via Slack message.

## Usage

### Installation

``` bash
git clone https://github.com/tym-xqo/pg_dba_metrics
pipenv install
```

### Configuration

#### Script config

Most script configuration is set via environment variables. The envars respected by pg_dba_metrics are as follows, or as shown in included [`.env.example`](.env_example):

- `METRIC_ENV`: indicates the environment in which you are running the script. `development` will cause the script to prefer settings in `.env` file; any other value will not override host environment variables if set
- `DATABASE_URL`: Postgres-format url string for connection to the main database to run metics against. Defaults to `postgres://postgres@localhost/yardstick` which probably isn't what you want 😉
- `STORE_DB_URL`: Optional url of secondary database in which to store metric time series. Defaults to same as `$DATABASE_URL`. Note this will create a `perf_metrics` table in the database if one is not present. Should connect as a user with permissions to create table
- `SLACK_TOKEN`: API token for Slack notifications
- `CHANNEL`: Slack channel or user id to send to. _Note that Slack settings have no defaults to fall back to_
- `HOSTNAME`: This is likely to be set for you already, but can be overridden in dev. Lets the script announce where it is posting from. Should correspond to the host in `$DATABASE_URL`
- `INTERVAL`: Time in seconds between checks in `schedule` mode. Default is 60.

#### Check and thresholds config

Metric checks are added by creating plain SQL files in local `query_files` directory. The pg_dba_script will search this directory in the working directory from which it is run. Generally, these are expected to be queries against [database stats tables](https://www.postgresql.org/docs/current/monitoring-stats.html) which return a single numeric value. (It is possible, however, for these queries to run any arbitrary SQL the operator may be interested in checking periodically.)

Thresholds for checks are set in a YAML front matter block before the query SQL, set off by `---` delimiters. The format is a status and a threshold definition, like so:

``` yaml
---
status: clear
threshold:
  field: <column name to find value in query result>
  gate: <a number at which alert will fire>
---
# SELECT ...

```

Note that the `alert` methods in the script report failure on a value greater than or equal to the threshold, in which case the `status` of the metric is automatically changed to `failure`. Failed metrics will send a `clear` alert and update status again when check value falls below the threshold. For queries that return multiple rows, we compare the highest value from all the results. _(I might want to add a feature to specify other comparison types, but that's work for a later version.)_

Any query may have alerting suspended by setting the status to `pause`, or by simply removing the 

### Operation

From the installation directory:

``` bash
python dba_metrics [-h] [-s] [-S] [name]
```

Arguments are all optional. Default behavior (no args) returns all metrics as JSON array of object(s) to stdout. `-s|--store` stores all metrics to table `perf_metrics` in the `$STORE_DB_URL` database, first creating the table if it doesn't already exist. `-S|--schedule` starts a blocking scheduler that executes the chosen output type once every `$INTERVAL` seconds. `name` defaults to `all` which will run all queries in the `query_files` directory in `$PWD` where script is run.
