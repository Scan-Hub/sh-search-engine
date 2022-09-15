# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from resources.health_check import HealthCheck
from resources.iapi import iapi_resources
from resources.explore.hot_keyword import HotKeywordResource
from resources.explore.trending import TrendingResource
from resources.explore.recently_add import RecentlyAddResource
from resources.explore.relatives import RelativesResource
from resources.query import QueryResource
from resources.custom_query import QueryCustomResource

api_resources = {
    '/common/health_check': HealthCheck,
    '/explore/hot_keyword': HotKeywordResource,
    '/explore/trending': TrendingResource,
    '/explore/recently_add': RecentlyAddResource,
    '/explore/relative': RelativesResource,
    
    '/query': QueryResource,
    '/query/custom': QueryCustomResource,

    **{f'/iapi{k}': val for k, val in iapi_resources.items()}
}
