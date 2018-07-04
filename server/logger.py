# coding=utf-8
# author=veficos

import logging
from fluent.asynchandler import FluentHandler
from fluent.handler import FluentRecordFormatter
from server.configs import configs


def __create_logger(conf):
    logger = logging.getLogger('da-service')
    level = logging.getLevelName(conf.level)
    logger.setLevel(level)

    __handler = FluentHandler(conf.fluent.tag, conf.fluent.host, conf.fluent.port)

    __handler.setFormatter(FluentRecordFormatter(fmt={
        'level': '%(levelname)s',
        'sys_host': '%(hostname)s',
        'sys_name': '%(name)s',
        'sys_module': '%(module)s',
        'function': '[%(pathname)s:%(funcName)s:%(lineno)d]',
        'stack_trace': '%(exc_text)s'
    }))
    __handler.setLevel(level)
    logger.addHandler(__handler)

    # 正式环境log.level等级
    if configs.env.deploy == 'dev':
        __stream_handler = logging.StreamHandler()
        __stream_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s [%(pathname)s:%(funcName)s:%(lineno)d] %(message)s'))
        __stream_handler.setLevel(level)
        logger.addHandler(__stream_handler)

    return logger

log = __create_logger(configs.remote.union.log)
