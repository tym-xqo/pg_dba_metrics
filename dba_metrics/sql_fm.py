#!/usr/bin/env python
# -*- coding: future_fstrings -*-
import os
import re

import yaml


def get_sql(name):
    """Read sql from file matching name and return as SQL string
    """
    query_file = os.path.join("query_files", name)
    with open(query_file) as f:
        query_sql = f.read()
    return query_sql


def parse_frontmatter(metric, with_sql=False):
    """Split metric sql on comment/yaml delimters and return metadata dict
    """
    bound = re.compile(r"^\/\*---$|^---\*\/$", re.MULTILINE)
    file = f"{metric['name']}.sql"
    sql = get_sql(file)
    parse = bound.split(sql, 2)
    try:
        metadata = yaml.safe_load(parse[1])
        if with_sql:
            sql = parse[-1].strip()
            return metadata, sql
        return metadata
    except IndexError:
        return None


def update_config(metric):
    """Rewrite sql metadata with new status after change
    """
    sql = parse_frontmatter(metric, True)[1]
    metadata = {
        key: metric[key] for key in ("check", "threshold", "status")
    }
    metadata_yaml = yaml.safe_dump(metadata)
    metadata_block = f"/*---\n{metadata_yaml}---*/"
    query_file = os.path.join("query_files", f"{metric['name']}.sql")
    with open(query_file, "w") as config_file:
        new_content = "\n".join([metadata_block, sql])
        config_file.write(new_content)