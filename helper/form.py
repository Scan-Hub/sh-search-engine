# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import random
import traceback
from config import Config
from helper.iapi_helper import IAPIHelper

from lib import dt_utcnow
from models import RawMetadataFeed, TokenHolderModel
from lib.exception import BadRequest
import pydash as py_
import bson
import requests


class FormHelper:

    @staticmethod
    def get_holder_info(smart_contracts):
        _return_data = []
        for _item in smart_contracts:
            _token_holder = TokenHolderModel.find_one({
                'contract': {
                        "$regex": py_.get(_item, 'contract', ''),
                        "$options": 'i'}
            })

            if _token_holder:
                _return_data.append({
                    'contract': py_.get(_item, 'contract'),
                    'chain': py_.get(_item, 'chain'),
                    'holders': py_.get(_token_holder, 'stats.holders', 0),
                    'holders_24h_gr': py_.get(_token_holder, 'gr.holders_24h_gr', 0)
                })

        return _return_data

    @staticmethod
    def get_latest_price_report_data(smart_contracts):
        _return_data = []
        for _item in smart_contracts:
            _metadata = RawMetadataFeed.find_one(
                {
                    'contract_address.contract_address': {
                        "$regex": py_.get(_item, 'contract', ''),
                        "$options": 'i'}
                }
            )
            _latest_data = py_.get(_metadata, 'quote.data.latest', [])
            _return_data.append({
                'contract': py_.get(_item, 'contract'),
                'chain': py_.get(_item, 'chain'),
                'data': _latest_data
            })

        return _return_data

