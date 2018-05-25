# -*- coding: utf-8 -*-

"""
全局对象
app：Flask对象
configs: 配置中心，读取zookeeper，转换对象
db: mysql数据库对象
redis：redis对象
log：日志对象
"""

from server.app import app
from server.configs import configs
from server.database import db, redis
from server.logger import log