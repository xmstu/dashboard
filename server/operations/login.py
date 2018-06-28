#!/usr/bin/python
# -*- coding:utf-8 -*-
# author=hexm
import hashlib

from flask_restful import abort

from server.cache_data import init_regions
from server.meta.session_operation import sessionOperationClass

from server.logger import log
from server.meta.decorators import make_decorator, Response
from server.models.login import Login
from server.status import make_result, HTTPStatus, APIStatus
from server.database import mongo
from server.models import RegionsModel
from server.database import db

class LoginDecorator(object):

    @staticmethod
    @make_decorator
    def common_check(user_name, password, role):
        """登录"""
        try:
            user_info = {}
            # 后台用户
            if role == 1:
                user_info = Login.get_user_by_admin(db.read_db, user_name, password)
            # 城市经理
            elif role == 4:
                user_info = Login.get_user_by_city_manage(db.read_bi, user_name, password)
            else:
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='用户身份错误'))

            if not user_info:
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='找不到该用户'))
            # 地区
            locations = []
            # 后台
            if role == 1:
                locations = [i for i in init_regions.region if init_regions.region[i]['level'] == 1]
            elif role == 4:
                locations = [user_info['region_id']]

            # 登录
            result = sessionOperationClass.insert(user_info, role, locations)

            return Response(result=result)
        except Exception as e:
            log.error('用户登录失败[error: %s]' % (e, ))
