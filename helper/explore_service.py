

from lib.utils import dt_utcnow
import json
from random import randint
import random
from datetime import datetime, timezone
from models import FormModel

def page_without_cache(filter, page_size: int, page: int, sort=1, func_sort=None, func_filter=None):
        _list = list(FormModel.find(filter=filter))
        if func_filter:
            _list = [x for x in _list if func_filter(x)]

        # if func_sort:
        #     if sort == 1:
        #         _list.sort(key=func_sort)
        #     else:
        #         _list.sort(key=func_sort, reverse=True)
                
        _offset = page_size * (page - 1)
        _limit = (int(page * page_size))
        _offset = int(_limit - page_size)
        result = _list[_offset:_limit]
        num_of_page = (len(_list) / page_size)
        if (len(_list) % page_size) > 0:
            num_of_page = num_of_page + 1

        return {
            "items": result,
            'num_of_page': num_of_page,
            'page_size': page_size,
            'page': page
        }    

    

class ExploreServiceHelper():
    
    
    @staticmethod
    def get_trending(params):
        
        _type = params['type']    
        # hard for mockup api
        _datetime_second = str(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()).split(".")[0] 
        _timezone = "UTC 0"            
        _trends = page_without_cache(filter={}, page=1, page_size=20)['items']
        _response = []
        for project in _trends:
            item = {
                'id' : str(project['_id']),
                'name': project['project_name'],
                'logo': project['project_logo'],
                "vote": project['vote_24h'],
            }
            _response.append(item)

        _response.sort(key=lambda s: s.get("vote"), reverse=True)
        _data = {
            "type": _type,
            "trends": _response,
            "from_datetime": _datetime_second,
            "timezone": _timezone
        }
        return _data

    
    
    @staticmethod
    def get_recently_add(params):
        
        _type = params['type']    
        _datetime_second = str(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()).split(".")[0] 

        _func_sort = lambda s: s.get("created_time")
        _projects_recently_add = page_without_cache(filter={}, page=1, page_size=3)['items']

        # _projects_recently_add = page_without_cache(filter={}, page=1, page_size=3, sort=1, func_sort=_func_sort)['items']
        _responses = []
        for project in _projects_recently_add:
            _projects = {
                'id' : str(project['_id']),
                'name': project['project_name'],
                'logo': project['project_logo'],
                'created_time': _datetime_second ,
            }
            _responses.append(_projects)
          
        return {                 
                'type' :  _type,
                "items": _responses
                }
    
    
    @staticmethod
    def get_relative_project(params):
        _type = params['type']    
        _func_sort = lambda s: s.get("_id")
        _projects_relative = page_without_cache(filter={}, page=1, page_size=20)['items']
        _datetime_second = str(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()).split(".")[0] 

        _responses = []
        for project in _projects_relative:
            _projects = {
                'id' : str(project['_id']),
                'name': project['project_name'],
                'description': project['project_description'],
                'logo': project['project_logo'],
                'created_time': _datetime_second ,
            }
            _responses.append(_projects)

        _responses = random.choices(_responses, k=4)	

        _data = {
            "type": _type,
            "items": _responses
        }
        
        return _data