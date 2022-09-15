# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from marshmallow import Schema, EXCLUDE, RAISE, fields, validate
from schemas.base import ResDatetimeField

_type_items = [
    "project",
    "teams",
    "company",
    "mkt_agency",
    "incubator"
]

class RelativeSchema(Schema):
    class Meta:
        unknown = RAISE

    type = fields.Str(required=True, validate=validate.OneOf(_type_items))


class ExploreItemResponse(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Str(required=True)
    name = fields.Str(required=True)
    logo = fields.Str(required=True)
    created_time = fields.Float(required=True)



class ExploreResponse(Schema):
    class Meta:
        unknown = EXCLUDE

    items = fields.List(fields.Nested(ExploreItemResponse))
    type = fields.Str(required=True)




