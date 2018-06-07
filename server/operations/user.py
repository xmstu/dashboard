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
        # 常驻地, 先去bi库筛选user_id
        user_station = None
        if params['home_station_id']:
            users = UserList.get_user_id_by_home_station(db.read_bi, params['home_station_id'])
            user_station = ','.join(users)
        # 用户详情
        user_list = UserList.get_user_list(db.read_db, page, limit, params, user_station)
        return Response(user_list=user_list)


class UserStatisticDecorator(object):

    @staticmethod
    @make_decorator
    def get_user_statistic(params):
        # 用户新增
        user_statistic = UserStatistic.get_user_statistic(db.read_bi, params)
        # 之前用户累计
        before_user_count = UserStatistic.get_before_user_count(db.read_bi, params)
        return Response(params=params, data=user_statistic, before_user_count=before_user_count)

