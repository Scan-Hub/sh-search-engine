# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from flask_restful import Resource

from connect import security
from schemas.query import QueryCustomSchema, QueryResponse
from helper.query import QueryHelper


class QueryCustomResource(Resource):

    @security.http(
        login_required=False,
        form_data=QueryCustomSchema(),
        response=QueryResponse()
    )
    def get(self, form_data, *args, **kwargs):
        res = QueryHelper.get_custom(form_data)
        return res
