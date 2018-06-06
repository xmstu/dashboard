# coding=utf-8
# author=veficos

from .meta.creators import DictModel
from .configs import configs
from .mysqldb import MySQLdb
from .mysqldb import MongoLinks


db = DictModel({
    'read_db': MySQLdb(dict(configs.remote.bi_dashboard.mysql.read_db.get())),
    'write_db': MySQLdb(dict(configs.remote.bi_dashboard.mysql.write_db.get())),
    'read_bi': MySQLdb(dict(configs.remote.bi_dashboard.mysql.read_bi.get())),
    'write_bi': MySQLdb(dict(configs.remote.bi_dashboard.mysql.write_bi.get()))
})

mongo = DictModel({
    'user_locations': MongoLinks(dict(configs.remote.bi_dashboard.mongo.user_locations.get()))
})

# redis = DictModel({
#     'token': pyredis.StrictRedis(connection_pool=pyredis.ConnectionPool(host=configs.remote.union.redis.token.host,
#                                                                         port=configs.remote.union.redis.token.port,
#                                                                         db=configs.remote.union.redis.token.db)),
#     'price_cacher': pyredis.StrictRedis(connection_pool=pyredis.ConnectionPool(host=configs.remote.union.redis.price_cache.host,
#                                                                                port=configs.remote.union.redis.price_cache.port,
#                                                                                db=configs.remote.union.redis.price_cache.db)),
# })
