#!/usr/bin/python
# -*- coding:utf-8 -*-

# Copyright (c) 2016 yu.liu <showmove@qq.com>
# All rights reserved
from flask import request
from server import log, read_db
from server.utils.extend import ExtendRedis
from server.models.general import TokenModel
from server import configs
access_expired = configs.remote.account_service.access_expired


def check_token_user(user_id, token) -> bool:
    assert str(user_id).isdigit()
    return get_user_id_by_token(token) == int(user_id)


def get_user_id_by_token(token):
    if not isinstance(token, str):
        return None
    log.info('token:{}'.format(token))
    token = token.replace('"', '').replace('\'', '')

    redis = ExtendRedis(db=1)
    result = redis.check_token(token)
    if result:
        return int(result)

    try:
        result = TokenModel.query_one(read_db, where_list=["token= '%s'" % token, 'is_deleted=0',
                                                           'expired_time >= UNIX_TIMESTAMP(NOW())'])
        if not(result and result.get('user_id')):
            return None
        redis.update_token(token, result['user_id'], expire_time=result['expired_time'])
        return result['user_id']

    except Exception as e:
        log.warning('System error : %s' % e, exc_info=True)
    return None


def get_user_id_by_mobile(mobile):
    result = read_db.query_one('SELECT id FROM shu_users WHERE mobile=:mobile AND is_deleted = 0', {'mobile': mobile})
    log.info('Result:%s ' % result)
    if result and result.get('id'):
        return result['id']
    else:
        return None


def check_device_id_disabled(device_id=None):
    """
    检测设备ID是否被禁用
    """
    if not device_id:
        device_id = request.headers.get('deviceId', 0)
    if device_id:
        dis = read_db.query_one('SELECT id FROM shu_device_blacklist WHERE device_id=:device_id AND is_deleted=0',
                                {'device_id': device_id})
        return bool(dis)
    return False


def check_mobile_disabled(mobile):
    """
    检测mobile是否被禁用
    """
    dis = read_db.query_one("""
    SELECT * FROM shu_user_profiles 
    WHERE `status` = -1 AND user_id IN (
        SELECT id FROM shu_users WHERE mobile=:mobile AND is_deleted=0) 
    """, {'mobile': mobile})
    return bool(dis)


def check_user_disabled(user_id):
    """
    检测user是否被禁用
    """
    # 检测状态码是否为-1(禁用)
    dis = read_db.query_one(""" SELECT * FROM shu_user_profiles WHERE `status` = -1 AND user_id =:user_id """,
                            {'user_id': user_id})
    return bool(dis)
