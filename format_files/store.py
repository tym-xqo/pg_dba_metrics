# -*- coding: utf-8 -*-
from marshmallow import Schema, fields


class ResultSchema(Schema):
    name = fields.Str(attribute="name")
    payload = fields.List(fields.Dict(), attribute="result")
    stamp = fields.Str(attribute="executed")
