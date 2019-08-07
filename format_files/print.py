# -*- coding: utf-8 -*-
from marshmallow import Schema, fields


class ResultSchema(Schema):
    name = fields.Str()
    result = fields.List(fields.Dict())
    status = fields.Str()
    threshold = fields.Dict()
    stamp = fields.Str(attribute="executed")
