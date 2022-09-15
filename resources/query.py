# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from flask_restful import Resource

from connect import security
from schemas.query import QuerySchema, QueryResponse
from helper.query import QueryHelper


class QueryResource(Resource):

    @security.http(
        login_required=False,
        params=QuerySchema(),
        response=QueryResponse()
    )
    def get(self, params, *args, **kwargs):
        
        res = QueryHelper.get(params)
        return res
