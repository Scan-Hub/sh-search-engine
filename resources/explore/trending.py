# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from flask_restful import Resource
from connect import security
from helper.explore_service import ExploreServiceHelper
from schemas.explore import RelativeSchema


class TrendingResource(Resource):

    @security.http(
        login_required=False,
        params=RelativeSchema()
    )
    def get(self, params):
       
        _result = ExploreServiceHelper.get_trending(params)
        _data = {
            "type": _result.get("type"), 
            "trends": _result.get("trends"), 
            "from_datetime": _result.get("from_datetime"),
            "from_timezone": _result.get("timezone")
        }
        
        return _data

   
