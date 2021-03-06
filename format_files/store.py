# -*- coding: utf-8 -*-
from marshmallow import Schema, fields


class ResultSchema(Schema):
    name = fields.Str()
    payload = fields.List(fields.Dict(), attribute="result")
    status = fields.Str()
    threshold = fields.Dict()
    stamp = fields.Str(attribute="executed")
