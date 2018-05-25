# coding=utf-8
# author=veficos

from .meta.creators import DictModel
from .configs import configs
from .mysqldb import MySQLdb

import redis as pyredis


db = DictModel({
        'reader': MySQLdb(dict(configs.remote.union.mysql.read_db.get())),
        'writer': MySQLdb(dict(configs.remote.union.mysql.write_db.get())),
    })

redis = DictModel({
    'token': pyredis.StrictRedis(connection_pool=pyredis.ConnectionPool(host=configs.remote.union.redis.token.host,
                                                                        port=configs.remote.union.redis.token.port,
                                                                        db=configs.remote.union.redis.token.db)),
    'price_cacher': pyredis.StrictRedis(connection_pool=pyredis.ConnectionPool(host=configs.remote.union.redis.price_cache.host,
                                                                               port=configs.remote.union.redis.price_cache.port,
                                                                               db=configs.remote.union.redis.price_cache.db)),
})
