# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
from config import Config
from lib import DaoModel, AsyncDaoModel
from connect import connect_db, redis_cluster, asyncio_mongo

__models__ = []

from models.user import UserDao

UserModel = UserDao(connect_db.db.users, redis=redis_cluster) # broker for write db with queue

AsyncUserModel = AsyncDaoModel(asyncio_mongo.db.users)
TokenHolderModel = UserDao(connect_db.db.token_holder)
FormModel = UserDao(connect_db.db.form, redis=redis_cluster) # broker for write db with queue
RawMetadataFeed = DaoModel(connect_db.db.raw_metadata_feed, redis=redis_cluster)

