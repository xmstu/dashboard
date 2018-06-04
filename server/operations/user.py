# -*- coding: utf-8 -*-

from server.database import db
from server.meta.decorators import make_decorator, Response
from server.models.user import UserList,UserStatistic


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
        if not params['region_id']:
            user_statistic = UserStatistic.get_user_statistic(db.read_db, params)
        return Response(data=user_statistic)

