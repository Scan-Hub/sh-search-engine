import requests
from config import Config
from models import TokenHolderModel
from web3 import Web3
from helper.form import FormHelper
import random
from helper.iapi_helper import IAPIHelper

_base_url = Config.ES_ACCESS_URL
_prefix_index = Config.ES_ACCESS_PREFIX_INDEX
headers = {}

_index_types = [
    {
        "type": "form",
        "index": f"{_prefix_index}.form",
        "fields": ["*"]
    },
    {
        "type": "user",
        "index": f"{_prefix_index}.users",
        "fields": ["display_name", "email", "address"]
    },
    {
        "type": "partner",
        "index": f"{_prefix_index}.kyc_partners",
        "fields": ["*"]
    },
    {
        "type": "news",
        "index": f"{_prefix_index}.news",
        "fields": ["*"]
    }
    
]

def get_must_queries(_params):
    _filter = []
    _queries = []
    if "category" in _params:
        _queries.append({
            "terms": { "category_type": [_params['category']] }
        })
    if "chain_id" in _params:
        _queries.append({
                "terms": { "smart_contracts.chain": [_params['chain_id']]  }
            })
    if "kyc" in _params:
        _queries.append({
                "term": { "kyc": _params['kyc']  }
            })
    if "entity" in _params:
        _queries.append({
            "terms": { "partner.name": [_params['entity']]  }
            })
    if "audit" in _params:
        _queries.append({
        "terms": { "audit_company": [_params['audit']]  }
        })    
    
    # Append must filter
    _filter.append({
    "bool": {
        "filter": _queries
        }
    })   
        
    if "ratings" in _params:
        _query = get_rating_query(_params['ratings'])   
        _filter.append(_query)    
    
    if "vote_range_min" in _params and "vote_range_max" in _params:    
        _filter.append(
            {
                "range": {
                    "total_vote": {
                    "gte":  _params['vote_range_min'],
                    "lte": _params['vote_range_max']
                    }
                }
            }
        )
                        
    return _filter
    
    
# 4- Rating
# + 8-10 : high
# + 5-8: medium
# + 3-5: low
# + < 3: lowest
_rating_query = {
    "high":{"min": 8 , "max": 10 } ,
    "medium":{"min": 5 , "max": 8 } ,
    "low":{"min": 3 , "max": 5 } ,
    "lowest":{"min": 0 , "max": 3 } 
}

def get_rating_query(ratings):
    _rating_queries = []
    for rating in ratings:
        _rating_option = _rating_query[rating]
        _query = {
            "range": {
                    "point": {
                    "gte":  _rating_option['min'],
                    "lte": _rating_option['max']
                    }
                }
        }
        _rating_queries.append(_query)
    
    return {
            "bool": {
                "should": _rating_queries
                }
            }
    
    
def get_index(_type):
    _filter =  list(filter(lambda obj: obj['type'] == _type, _index_types))
    return _filter[0]


def format_index_response(type, _data):
    _hits = _data['hits']['hits']
    items = []
    _items_by_type = []
    for item in _hits:
        _source = item['_source']
        _item = {}
        
        _item = {
            "_id": item['_id'],
            **_source
        }
   
        _items_by_type.append(_item) 
    
    items.append(
            {
            "type": type,
            "items": _items_by_type
            }
        )     
        
    return  _items_by_type        
                 
        
class QueryHelper():
    

    @staticmethod
    def get(_params):
        _list_index_filter = []
        if "type" not in _params:
            _list_index_filter = _index_types
                
        else:    
            _index = get_index(_params["type"])
            _list_index_filter.append(_index)
            
        
        # list result filter
        items = []
        for _index_filter in _list_index_filter:
            _body = {
        
                "query": {
                    "query_string": {
                        "query": f"*{_params['query']}*",
                        "fields": _index_filter['fields']
                    }
                },
                "size": _params['limit'],
                "from": _params['offset'],
                "sort": []
            }
        
            # Get from API
            response = requests.get(f"{_base_url}/{_index_filter['index']}/_search", json=_body, headers=headers)
            response_data = response.json()
            
            _items = format_index_response(_index_filter["type"], response_data)  

            items.append({
                "type": _index_filter["type"],
                "items": _items })  
            
        return { "result": items }
    
    
    
    
    @staticmethod
    def get_custom(_params):
        _list_index_filter = []
        if "type" not in _params:
            _list_index_filter = _index_types
                
        else:    
            _index = get_index(_params["type"])
            _list_index_filter.append(_index)
            
        
        # list result filter
        items = []
        _filters = get_must_queries(_params)
        for _index_filter in _list_index_filter:
            _body = {
        
               "query": {
                    "bool": {
                    "filter": _filters
                    }
                },
                "sort": []
            }
        
            # Get from API
            response = requests.get(f"{_base_url}/{_index_filter['index']}/_search", json=_body, headers=headers)
            response_data = response.json()
            
            _items = format_index_response(_index_filter["type"], response_data)  
            # filter holders
            if "holder_range_min" in _params and "holder_range_max" in _params \
                and _params['holder_range_min'] and _params['holder_range_max']:  

                _contracts_items = []
                for item in _items:
                   _item_smart_contracts =  item['smart_contracts'] 
                   if len(_item_smart_contracts) > 0:
                       for sc in _item_smart_contracts:
                            
                            _contracts_items.append(str(sc['contract']).lower())
                           
                _filter_holder = {
                    "$and": [
                        {"stats.holders": {
                            "$gte": _params["holder_range_min"],
                            "$lte": _params["holder_range_max"]
                            }
                        },
                        {"$or": [
                            {"contract": {"$in": _contracts_items}},
                            {"eth_contract": {"$in": _contracts_items}},
                        ]
                        }
                    ]
                }

                _token_holders = list(TokenHolderModel.find(filter = _filter_holder))
                _result_filter_holder = []
                for holder in _token_holders:
                    for item in _items:
                        _smart_contracts = item['smart_contracts']
                        for contract in _smart_contracts:
                            _contract_address = contract['contract'].lower()
                            
                            if  _contract_address == str(holder['contract']).lower() \
                                or _contract_address == str(holder['eth_contract']).lower() :
                                _result_filter_holder.append(item)
                _items = _result_filter_holder

            # set limit, offset for response
            _limit =  _params['page_size']
            _offset =  _params['page'] - 1
            result = _items[_offset:_limit]
            num_of_page = int(len(_items) / _limit)
            if (len(result) % _limit) > 0:
                num_of_page = num_of_page + 1
            
                
            _return_items = []
            for _project in result:
                _smart_contracts = _project['smart_contracts']

                # get project holders information
                _holders = FormHelper.get_holder_info(
                    smart_contracts=_smart_contracts)

                _project['holders'] = _holders

                _latest_price_report = FormHelper.get_latest_price_report_data(smart_contracts=_smart_contracts)
                _project['latest_price_report'] = _latest_price_report

                #FIXME: random field for MVP version
                _project['watch_list_number'] = random.randrange(101, 9999)

                # get coin market cap information
                if not _smart_contracts:
                    _return_items.append(_project)
                    continue

                _token_info = IAPIHelper.get_token_info(
                    smart_contract_address=_smart_contracts[0]['contract'])

                _project = {
                    **_project,
                    **_token_info
                }

                _return_items.append(_project)
            
            items.append(
                {
                "type": _index_filter["type"],
                "items": _return_items ,
                "page": _params['page'],
                "page_size": _params['page_size'],
                "num_of_page": num_of_page,
                }
                )  
            
        return { "result": items }
        