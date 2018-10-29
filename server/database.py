# coding=utf-8
# author=veficos
from werkzeug.contrib.cache import RedisCache

from server.configs import configs
from server.meta.creators import DictModel
from server.db import MongoLinks
from server.db import MySQLdb


mongo = DictModel({
    'user_locations': MongoLinks(config=dict(configs.remote.union.mongo.locations.get()), collection='user_locations')
})


redis_cache_conn = RedisCache(host=configs.get("redis_host", "127.0.0.1"),
                              port=configs.get("redis_port", 6309),
                              db=configs.get("db", 1))
