# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from marshmallow import Schema, EXCLUDE, RAISE, fields, validate
from schemas.base import NotBlank

_type_items = [
    "user",
    "form",
    "partner",
    "news",
]

_type_items_custom = [
    "form",
]

_ratings = [
    "high",
    "medium",
    "low",
    "lowest"
]

class QuerySchema(Schema):
    class Meta:
        unknown = RAISE

    type = fields.Str(required=False, validate=validate.OneOf(_type_items))
    query = fields.Str(required=True, validate=NotBlank())
    limit = fields.Int(required=False, default=20)
    offset = fields.Int(required=False, default=0)


class QueryCustomSchema(Schema):
    class Meta:
        unknown = RAISE

    type = fields.Str(required=False, validate=validate.OneOf(_type_items_custom))
    
    chain_id = fields.Str(required=False, validate=NotBlank())
    category = fields.Str(required=False, validate=NotBlank())
    entity = fields.Str(required=False, validate=NotBlank())
    kyc = fields.Bool(required=False)
    audit = fields.Str(required=False, validate=NotBlank())
    vote_range_min = fields.Float(required=False, default=0)
    vote_range_max = fields.Float(required=False, default=1000000000)
    holder_range_min = fields.Float(required=False, default=0)
    holder_range_max = fields.Float(required=False, default=1000000000)
    ratings = fields.List(fields.Str(required=False, validate=validate.OneOf(_ratings)))
    
    page_size = fields.Int(required=False, default=10)
    page = fields.Int(required=False, default=1)
    
    

class QueryItemResponse(Schema):
    class Meta:
        unknown = EXCLUDE

    items = fields.List(fields.Dict())
    type = fields.Str(required=True)
    page_size = fields.Int(required=True)
    page = fields.Int(required=True)
    num_of_page = fields.Int(required=True)


class QueryResponse(Schema):
    class Meta:
        unknown = EXCLUDE

    result = fields.List(fields.Dict())




