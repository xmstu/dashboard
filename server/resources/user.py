#!/usr/bin/python
# -*- coding:utf-8 -*-
# author=hexm
import time

from flask_restful import Resource

import server.document.user as doc
from server import api, log
from server import verify, operations, filters
from server.database import db
from server.meta.decorators import Response
from server.models.user import UserQuery
from server.utils.request import get_payload


class User(Resource):

    def get(self):
        area = UserQuery.get_area(db.read_io)
        return area

    def post(self):
        payload = get_payload()
        start_time = payload.get('start_time', '')
        end_time = payload.get('end_time', '')
        periods = payload.get('periods', '')
        user_type = payload.get('user_type', '')

        role = payload.get('role', '')
        region_id = payload.get('region_id', '')
        is_auth = payload.get('is_auth', '')

        resp = Response()


class UserStatistic(object):

    @verify.User.get
    def get(self):
        payload = get_payload()

        resp = Response()


class UserList(object):

    @doc.request_user_list_param
    @doc.response_user_list_param_success
    @filters.UserList.get()
    @operations.UserListDecorator.get(user_name=str, mobile=str, reference_mobile=str, download_channel=str,
                                      from_channel=str,
                                      is_referenced=int, home_station_id=int, role_type=int, role_auth=int,
                                      is_actived=int,
                                      is_used=int, is_car_sticker=int, index=int, count=int,
                                      last_login_start_time=int, last_login_end_time=int,
                                      register_start_time=int, register_end_time=int)
    @verify.UserList.get(user_name=str, mobile=str, reference_mobile=str, download_channel=str, from_channel=str,
                         is_referenced=int, home_station_id=int, role_type=int, role_auth=int, is_actived=int,
                         is_used=int, is_car_sticker=int, index=int, count=int,
                         last_login_start_time=int, last_login_end_time=int,
                         register_start_time=int, register_end_time=int
                         )
    def get(self):
        payload = get_payload()
        user_name = payload.get('user_name', '')
        mobile = payload.get('mobile', '')
        reference_mobile = payload.get('reference_mobile', '')
        download_channel = payload.get('download_channel', '')
        from_channel = payload.get('from_channel', '')
        is_referenced = payload.get('is_referenced', 0)
        home_station_id = payload.get('home_station_id', 0)
        role_type = payload.get('role_type', 0)
        role_auth = payload.get('role_auth', 0)
        is_actived = payload.get('is_actived', 0)
        is_used = payload.get('is_used', 0)
        is_car_sticker = payload.get('is_car_sticker', 0)
        index = payload.get('index', 1)
        count = payload.get('count', 10)

        last_login_start_time = payload.get('last_login_start_time', int(time.time()))
        last_login_end_time = payload.get('last_login_end_time', int(time.time()))

        register_start_time = payload.get('register_start_time', int(time.time()))
        register_end_time = payload.get('register_end_time', int(time.time()))

        resp = Response(user_name=user_name, mobile=mobile, reference_mobile=reference_mobile,
                        download_channel=download_channel, from_channel=from_channel, is_referenced=is_referenced,
                        home_station_id=home_station_id, role_type=role_type, role_auth=role_auth,
                        is_actived=is_actived, is_used=is_used, is_car_sticker=is_car_sticker, index=index, count=count,
                        last_login_start_time=last_login_start_time, last_login_end_time=last_login_end_time,
                        register_start_time=register_start_time, register_end_time=register_end_time)

        log.info('获取用户列表查询参数: [resp: {}]'.format(resp))
        return resp


ns = api.namespace('user', description='用户统计')
ns.add_resource(User, '/user/')
ns.add_resource(UserStatistic, '/user/statistic/')
ns.add_resource(UserList, '/user/list/')
