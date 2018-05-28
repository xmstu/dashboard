#!/usr/bin/python
# -*- coding:utf-8 -*-
# author=hexm
import time

from flask import session

from server.status import HTTPStatus, APIStatus, build_result
from server.meta.decorators import make_decorator


class Login(object):

    @staticmethod
    @make_decorator
    def post(user_info):
        session['login'] = {
            'user_id': user_info['id'],
            'mobile': user_info['mobile'],
            'login_time': time.time()
        }
        return build_result(APIStatus.Ok, data=''), HTTPStatus.Ok
