#!/usr/bin/python
# -*- coding:utf-8 -*-
# author=hexm
from flask_restful import abort

from server.cache_data import init_regions
from server.meta.session_operation import sessionOperationClass

from server.logger import log
from server.meta.decorators import make_decorator, Response
from server.models.login import Login
from server.status import make_result, HTTPStatus, APIStatus
from server.database import db


class LoginDecorator(object):

    @staticmethod
    @make_decorator
    def common_check(user_name, password):
        """登录"""
        try:
            # 管理员用户
            user_info = Login.get_user_by_admin(db.read_bi, user_name, password)
            if not user_info:
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.NotUser, msg='找不到该用户'))
            # 后台
            if '1' == user_info['region_id']:
                locations = [i for i in init_regions.region if init_regions.region[i]['level'] == 1]
            else:
                locations = user_info['region_id']

            user_info['account'] = user_name
            # 写入session
            result = sessionOperationClass.insert(user_info, locations)
            return Response(result=result)
        except Exception as e:
            log.error('用户登录失败[error: %s]' % (e, ), exc_info=True)
