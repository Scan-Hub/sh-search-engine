# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from flask_restful import Resource
from connect import security


class HotKeywordResource(Resource):

    @security.http(
        login_required=False
    )
    def get(self):
       
        _data = {
            'type': 'project',
            "keywords": [
                "#defi",
                "#gamefi",
                "#innovation",
                "#metaverse"
            ]
        }
        return _data

   
