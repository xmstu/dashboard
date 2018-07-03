# -*- coding: utf-8 -*-

from flask_restful import abort

from server.meta.decorators import make_decorator, Response
from server.models.user import UserList,UserStatistic
from server.status import HTTPStatus, make_result, APIStatus
from server.database import mongo
from server.models import RegionsModel
from server.database import db


class UserListDecorator(object):

    @staticmethod
    @make_decorator
    def get_user_list(page, limit, params):
        # 用户详情
        user_list = UserList.get_user_list(db.read_bi, page, limit, params)
        return Response(user_list=user_list)


class UserStatisticDecorator(object):

    @staticmethod
    @make_decorator
    def get_user_statistic(params):
        """用户变化趋势统计"""
        # 用户常驻地
        user_ids = None
        if params['region_id']:
            # 用户自选
            if isinstance(params['region_id'], int):
                user_ids = UserList.get_user_home_station_by_int(db.read_bi, params['region_id'])
            # 非管理员默认地区
            elif isinstance(params['region_id'], list):
                user_ids = UserList.get_user_home_station_by_list(db.read_bi, params['region_id'])

        user_statistic = UserStatistic.get_user_statistic_by_mobile(db.read_db, params, user_ids)
        before_user_count = 0
        if params['user_type'] == 2:
            before_user_count = UserStatistic.get_before_user_count_by_mobile(db.read_db, params, user_ids)
        # 用户新增
        # user_statistic = UserStatistic.get_user_statistic(db.read_bi, params)
        # 用户累计
        # before_user_count = UserStatistic.get_before_user_count(db.read_bi, params)
        return Response(params=params, data=user_statistic, before_user_count=before_user_count)

