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
        user_list = UserList.get_user_list(db.read_db, page, limit, params)
        return Response(user_list=user_list)


class UserStatisticDecorator(object):

    @staticmethod
    @make_decorator
    def get_user_statistic(params):
        # 地区
        user_statistic = UserStatistic.get_user_statistic(db.read_bi, params)
        return Response(params=params, data=user_statistic)

