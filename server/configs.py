# -*- coding: utf-8 -*-

from server.superconf import SuperConf
from server.superconf.jsonserialize import JsonSerialize
from server.superconf.kazooengine import KazooEngine
from server.superconf.engine import Engine

import os

# 读取zookeeper中配置文件
configs = SuperConf(serialize=JsonSerialize(remote_filename=''.join([str(os.getpid()), '-', 'superconf.json'])),
                    engine=KazooEngine(
                        hosts=SuperConf(JsonSerialize(), engine=Engine()).env.zookeeper.host
                        ), root='superconf')

@configs.register('.union.mysql.read_db')
def __read_db(conf):
    pass


@configs.register('.union.mysql.write_db')
def __write_db(conf):
    pass


@configs.register('.union.log')
def __log(conf):
    pass


@configs.register('.union.redis.token')
def __token(conf):
    pass


@configs.register('.union.redis.price_cache')
def __cache(conf):
    pass


@configs.register('.union.service_urls')
def __service_urls(conf):
    pass


@configs.register('.union.urls')
def __urls(conf):
    pass


@configs.register('.union.shorturl')
def __shorturl(conf):
    pass


@configs.register('.union.messager')
def __messager(conf):
    pass


@configs.register('.union.open_event')
def __open_event(conf):
    pass


@configs.register('.feed_service')
def __feed_service(conf):
    pass
