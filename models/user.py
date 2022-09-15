# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from lib import DaoModel


class UserDao(DaoModel):
    def __init__(self, *args, **kwargs):
        super(UserDao, self).__init__(*args, **kwargs)

    def user_of_address(self, address, upsert=False):
        _user = self.find_one({
            'public_address': address
        })
        return _user
