import requests

import pydash as py_

from config import Config


class IAPIHelper(object):
    
    
    @staticmethod
    def get_token_info(smart_contract_address):
        if not smart_contract_address:
            return {}
        TOKEN_INFO_URL = f'{Config.SH_API_URL}/v1/metadata-feed/query?address={smart_contract_address}'
        _response = requests.get(TOKEN_INFO_URL)
        if not _response.status_code == 200 or not _response.json()['data']:
            return {}
        _data = _response.json()['data']
        return {
            'chain': py_.get(_data, 'platform.name', ''),
            'cmc_project_id': py_.get(_data, 'id'),
            'cmc_name': py_.get(_data, 'name', ''),
            'cmc_symbol': py_.get(_data, 'symbol', ''),
            'cmc_logo': py_.get(_data, 'logo', ''),
            'cmc_date_launched': py_.get(_data, 'date_launched', '')
        }
