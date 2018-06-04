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
        user_id = []
        if params['region_id']:
            three_region = RegionsModel.get_three_area(db.read_db, params['region_id'])
            if not three_region:
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='地区选择错误'))
            if three_region['first_code']:
                region = {
                    'province_id': three_region['first_code'],
                    'city_id': three_region['second_code'],
                    'county_id': three_region['third_code']
                }
            else:
                region = {
                    'province_id': three_region['second_code'],
                    'city_id': three_region['third_code']
                }
            result = mongo.user_locations.collection.aggregate([{
                '$match': region
                },
                {'$group': {'_id': {'province_id': '$province_id', 'city_id': '$city_id', 'county_id': '$county_id'}, 'scores': {'$addToSet': '$user_id'}}
            }])
            for i in result:
                user_id.extend(i['scores'])
            user_id = list(set(user_id))
        user_statistic = UserStatistic.get_user_statistic(db.read_db, params, user_id)
        return Response(params=params, data=user_statistic)

