# -*- coding: utf-8 -*-

"""
全局对象
app：flask对象
api：flask_restplus对象
configs: 配置中心，读取zookeeper，转换对象
db: mysql数据库对象
redis：redis对象
log：日志对象
"""

from server.app import app, api
from server.configs import configs
from server.database import db
from server.db import MySQLdb
from server.logger import log

# 加载flask路由和flask_restplus资源接口
import server.route
import server.resources
from server.utils import Model

modules = Model({
    'read_db': MySQLdb(dict(configs.remote.union.mysql.read_db.get())),
    'write_db': MySQLdb(dict(configs.remote.union.mysql.write_db.get())),
    'log': logger
})

log = modules['log']
read_db = modules['read_db']
write_db = modules['write_db']
