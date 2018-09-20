#!/usr/bin/python
# -*- coding:utf-8 -*-
# author=hexm
import time

from flask_restful import abort
from server.status import HTTPStatus, APIStatus, make_resp
from server.meta.decorators import make_decorator


class Login(object):

    @staticmethod
    @make_decorator
    def insert_session(result):
        if result:
            return make_resp(APIStatus.Ok), HTTPStatus.Ok
        else:
            abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.InternalServerError, msg='登录失败'))

