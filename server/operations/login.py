#!/usr/bin/python
# -*- coding:utf-8 -*-
# author=hexm
from server.models.login import Login
from server.meta.decorators import make_decorator, Response
from server.database import db
from server.status import make_result, HTTPStatus, APIStatus

from flask_restful import abort
import hashlib

class LoginDecorator(object):

    def __init__(self):
        pass

    @staticmethod
    @make_decorator
    def common_check(user_name, password):
        password = hashlib.md5(password.encode('utf8')).hexdigest()
        user_info = Login.get_user(db.read_io, user_name, password)
        if not user_info:
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='找不到该用户'))
        return Response(user_info=user_info)
