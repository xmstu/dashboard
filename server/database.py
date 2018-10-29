# coding=utf-8
# author=veficos
from werkzeug.contrib.cache import RedisCache

from server.configs import *
from server.meta.creators import DictModel
import pymongo
from server.db import MySQLdb


mongo_conn = pymongo.MongoClient(host=MONGO_HOST,
                                 port=MONGO_PORT
                                 )


redis_cache_conn = RedisCache(host=REDIS_HOST,
                              port=REDIS_PORT,
                              db=REDIS_DB)
