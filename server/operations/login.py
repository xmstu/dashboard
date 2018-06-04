#!/usr/bin/python
# -*- coding:utf-8 -*-
# author=hexm
import hashlib

from flask_restful import abort
from flask import session

from server.meta.decorators import make_decorator, Response
from server.models.login import Login
from server.status import make_result, HTTPStatus, APIStatus
from server.database import mongo
from server.models import RegionsModel
from server.database import db

class LoginDecorator(object):

    def __init__(self):
        pass

    @staticmethod
    @make_decorator
    def common_check(user_name, password, role):
        # 后台用户
        if role == 1:
            user_info = Login.get_user_by_admin(db.read_db, user_name, password)
        # 区镇合伙人 & 网点管理
        elif role == 2 or role == 3:
            password = hashlib.md5(password.encode('utf8')).hexdigest()
            user_info = Login.get_user_by_user(db.read_db, user_name, password)
        # TODO 城市经理
        elif role == 4:
            pass
        else:
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='用户身份错误'))
        # 地区
        locations = []
        # 后台
        if role == 1:
            result = mongo.user_locations.collection.aggregate([{
                '$group': {'_id': {'province_id': '$province_id', 'city_id': '$city_id', 'county_id': '$county_id'}}
            }])
            for location in result:
                region_name = {}
                # 存在市、区
                if location['_id']['county_id']:
                    region_name = RegionsModel.get_region_by_code(db.read_db, location['_id']['county_id'])
                elif location['_id']['city_id']:
                    region_name = RegionsModel.get_region_by_code(db.read_db, location['_id']['city_id'])
                if region_name and region_name['full_short_name']:
                    locations.append({
                        'region_id': region_name['code'],
                        'name': region_name['full_short_name']
                    })
        # 区镇合伙人
        elif role == 2:
            result = RegionsModel.get_user_region(db.read_db, session['user_id'])
            for location in result:
                if location['region_id'] and location['full_short_name']:
                    locations.append({
                        'region_id': location['region_id'],
                        'name': location['full_short_name']
                    })
        # 排序
        locations.sort(key=lambda x: x['region_id'])

        if not user_info:
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='找不到该用户'))

        return Response(user_info=user_info, role=role, locations=locations)
