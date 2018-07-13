# coding=utf-8
# author=veficos

from server.meta.creators import DictModel
from server.configs import configs
from server.mysqldb import MySQLdb
from server.mysqldb import MongoLinks
from server.mysqldb import ExtendRedis

db = DictModel({
    'read_db': MySQLdb(dict(configs.remote.union.mysql.read2_db.get())),
    'write_db': MySQLdb(dict(configs.remote.union.mysql.write_db.get())),
    'read_bi': MySQLdb(dict(configs.remote.union.mysql.da_read_db.get())),
    'write_bi': MySQLdb(dict(configs.remote.union.mysql.da_write_db.get()))
})
# 不创建全局对象, 节省资源
# mongo = DictModel({
#     'user_locations': MongoLinks(config=dict(configs.remote.union.mongo.locations.get()), collection='user_locations')
# })

pyredis = DictModel({
    'token': ExtendRedis(ip=configs.remote.union.redis.token.host,
                          port=configs.remote.union.redis.token.port,
                          db=configs.remote.union.redis.token.db)
})

# redis = DictModel({
#     'token': pyredis.StrictRedis(connection_pool=pyredis.ConnectionPool(host=configs.remote.union.redis.token.host,
#                                                                         port=configs.remote.union.redis.token.port,
#                                                                         db=configs.remote.union.redis.token.db)),
#     'price_cacher': pyredis.StrictRedis(connection_pool=pyredis.ConnectionPool(host=configs.remote.union.redis.price_cache.host,
#                                                                                port=configs.remote.union.redis.price_cache.port,
#                                                                                db=configs.remote.union.redis.price_cache.db)),
# })
