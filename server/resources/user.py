#!/usr/bin/python
# -*- coding:utf-8 -*-
# author=hexm

from flask_restplus.resource import Resource

import server.document.user as doc
from server import api, log
from server.filters import user_list_get_result, get_behavior_result, user_statistic_get_result
from server.meta.redis_cache import redis_cache
from server.operations import get_user_list, get_user_behavior_statistic, get_user_statistic
from server.utils.request import *
from server.verify import user_list_check_params, check_behavior_params, user_statistic_check_params


class UserStatistic(Resource):
    @doc.request_user_statistic_param
    @redis_cache(expire_time=7200)
    def get(self):
        """用户变化趋势"""
        params = user_statistic_check_params(params=get_all_arg())
        log.info('获取用户变化趋势查询参数: [resp: {}]'.format(params))
        user_statistic, before_user_count = get_user_statistic(params)
        return user_statistic_get_result(params, user_statistic, before_user_count)


class UserBehaviorStatistic(Resource):
    @doc.request_user_behavior_statistic_param
    @redis_cache(expire_time=7200)
    def get(self):
        """用户行为变化趋势"""
        params = check_behavior_params(params=get_all_arg())
        data = get_user_behavior_statistic(params)
        return get_behavior_result(params, data)


class UserList(Resource):

    @doc.request_user_list_param
    @redis_cache(expire_time=7200)
    def get(self):
        """用户列表"""
        params = user_list_check_params(params=get_all_arg())
        log.info('获取用户列表查询参数: [resp: {}]'.format(params))
        user_list = get_user_list(params)
        return user_list_get_result(user_list)


ns = api.namespace('user', description='用户统计')
ns.add_resource(UserStatistic, '/statistic/')
ns.add_resource(UserBehaviorStatistic, '/behavior_statistic/')
ns.add_resource(UserList, '/list/')
