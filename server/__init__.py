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
from server.utils import Model

modules = Model({
    'read_prod': MySQLdb(dict(configs.remote.bi_dashboard.mysql.read_prod.get())),
    'read_bi': MySQLdb(dict(configs.remote.bi_dashboard.mysql.read_bi.get())),
    'write_bi': MySQLdb(dict(configs.remote.bi_dashboard.mysql.write_bi.get())),
    'read_io': MySQLdb(dict(configs.remote.bi_dashboard.mysql.read_io.get())),
    'write_io': MySQLdb(dict(configs.remote.bi_dashboard.mysql.write_io.get())),
})

read_io = modules['read_io']
write_io = modules['write_io']

# 加载flask路由和flask_restplus资源接口
import server.route
import server.resources