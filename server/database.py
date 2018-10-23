# coding=utf-8
# author=veficos
from werkzeug.contrib.cache import RedisCache

from server.configs import configs
from server.meta.creators import DictModel
from server.mysqldb import ExtendRedis
from server.mysqldb import MySQLdb

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
                         db=configs.remote.union.redis.token.db),
})

redis_cache_conn = RedisCache(host=configs.remote.union.redis.da_cacher.host,
                              port=configs.remote.union.redis.da_cacher.port,
                              db=configs.remote.union.redis.da_cacher.db)
