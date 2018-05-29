#!/usr/bin/python
# -*- coding:utf-8 -*-
# author=hexm
import time

from flask_restplus.resource import Resource

import server.document.user as doc
from server import api, log, document
from server import verify, operations, filters
from server.database import db
from server.meta.decorators import Response
from server.models.user import UserQuery
from server.utils.request import *


# class User(Resource):
#
#     def get(self):
#         area = UserQuery.get_area(db.read_io)
#         return area
#
#     def post(self):
#         payload = get_payload()
#         start_time = payload.get('start_time', '')
#         end_time = payload.get('end_time', '')
#         periods = payload.get('periods', '')
#         user_type = payload.get('user_type', '')
#
#         role = payload.get('role', '')
#         region_id = payload.get('region_id', '')
#         is_auth = payload.get('is_auth', '')
#
#         resp = Response()


# class UserStatistic(Resource):
#
#     @verify.User.get
#     def get(self):
#         payload = get_payload()
#
#         resp = Response()


class UserList(Resource):

    @staticmethod
    @doc.request_user_list_param
    @doc.response_user_list_param_success
    @filters.UserList.get(user_list=dict)
    @operations.UserListDecorator.get_user_list(pages=int, limit=int, params=dict)
    @verify.UserList.check_params(pages=int, limit=int, params=dict)
    @verify.UserList.check_paging(pages=int, limit=int, params=dict)
    def get():

        resp = Response(pages=get_arg_int('pages', 1),
                        limit=get_arg_int('limit', 10),
                        params=get_all_arg())

        log.info('获取用户列表查询参数: [resp: {}]'.format(resp))
        return resp


ns = api.namespace('user', description='用户统计')
# ns.add_resource(User, '/user/')
# ns.add_resource(UserStatistic, '/statistic/')
ns.add_resource(UserList, '/list/')
