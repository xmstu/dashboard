#!/usr/bin/python
# -*- coding:utf-8 -*-
# author=hexm
import hashlib

from flask_restful import abort

from server.database import db
from server.meta.decorators import make_decorator, Response
from server.models.login import Login
from server.status import make_result, HTTPStatus, APIStatus


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

        if not user_info:
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='找不到该用户'))

        return Response(user_info=user_info, role=role)
