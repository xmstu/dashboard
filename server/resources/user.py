#!/usr/bin/python
# -*- coding:utf-8 -*-
# author=hexm

from flask_restplus.resource import Resource

import server.document.user as doc
import server.verify.general as general_verify
from server import api, log
from server import verify, operations, filters
from server.meta.decorators import Response
from server.utils.request import *


class UserStatistic(Resource):
    @staticmethod
    @doc.request_user_statistic_param
    @doc.response_user_statistic_param_success
    @filters.UserStatistic.get_result(params=dict, data=list, before_user_count=int)
    @operations.UserStatisticDecorator.get_user_statistic(params=dict)
    @verify.UserStatistic.check_params(params=dict)
    def get():

        resp = Response(params=get_all_arg())

        log.info('获取用户变化趋势查询参数: [resp: {}]'.format(resp))
        return resp


class UserList(Resource):

    @staticmethod
    @doc.request_user_list_param
    @doc.response_user_list_param_success
    @filters.UserList.get(user_list=dict)
    @operations.UserListDecorator.get_user_list(page=int, limit=int, params=dict)
    @verify.UserList.check_params(page=int, limit=int, params=dict)
    @general_verify.Paging.check_paging(page=int, limit=int, params=dict)
    def get():

        resp = Response(page=get_arg_int('page', 1),
                        limit=get_arg_int('limit', 10),
                        params=get_all_arg())

        log.info('获取用户列表查询参数: [resp: {}]'.format(resp))
        return resp


ns = api.namespace('user', description='用户统计')
ns.add_resource(UserStatistic, '/statistic/')
ns.add_resource(UserList, '/list/')
