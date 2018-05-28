# coding=utf-8
# author=veficos

from .meta.creators import DictModel
from .configs import configs
from .mysqldb import MySQLdb


db = DictModel({
    'read_prod': MySQLdb(dict(configs.remote.bi_dashboard.mysql.read_prod.get())),
    'read_bi': MySQLdb(dict(configs.remote.bi_dashboard.mysql.read_bi.get())),
    'write_bi': MySQLdb(dict(configs.remote.bi_dashboard.mysql.write_bi.get())),
    'read_io': MySQLdb(dict(configs.remote.bi_dashboard.mysql.read_io.get())),
    'write_io': MySQLdb(dict(configs.remote.bi_dashboard.mysql.write_io.get())),
})

# redis = DictModel({
#     'token': pyredis.StrictRedis(connection_pool=pyredis.ConnectionPool(host=configs.remote.union.redis.token.host,
#                                                                         port=configs.remote.union.redis.token.port,
#                                                                         db=configs.remote.union.redis.token.db)),
#     'price_cacher': pyredis.StrictRedis(connection_pool=pyredis.ConnectionPool(host=configs.remote.union.redis.price_cache.host,
#                                                                                port=configs.remote.union.redis.price_cache.port,
#                                                                                db=configs.remote.union.redis.price_cache.db)),
# })
