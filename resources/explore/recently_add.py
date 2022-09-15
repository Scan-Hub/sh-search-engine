# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from flask_restful import Resource
from connect import security
from helper.explore_service import ExploreServiceHelper
from schemas.explore import RelativeSchema, ExploreResponse


class RecentlyAddResource(Resource):

    @security.http(
        login_required=False,
        params=RelativeSchema(),
        response=ExploreResponse()
    )
    def get(self, params):
       
        _result = ExploreServiceHelper.get_recently_add(params)
   
        return _result

   
