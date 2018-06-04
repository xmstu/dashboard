#!/usr/bin/python
# -*- coding:utf-8 -*-
# author=hexm
import time

from flask import session

from server.status import HTTPStatus, APIStatus, make_result
from server.meta.decorators import make_decorator
import simplejson as json

class Login(object):

    @staticmethod
    @make_decorator
    def post(user_info, role):
        session['login'] = {
            'user_id': user_info['id'],
            'user_name': user_info['user_name'] if user_info['user_name'] else '',
            'mobile': user_info['mobile'],
            'avatar_url': user_info['avatar_url'] if user_info['avatar_url'] else 'https://mp.huitouche.com/static/images/newicon.png',
            'login_time': time.time(),
            'role': role
        }
        data = {
            'user_name': user_info['user_name'] if user_info['user_name'] else '',
            'avatar_url': user_info['avatar_url'] if user_info['avatar_url'] else 'https://mp.huitouche.com/static/images/newicon.png'
        }
        return make_result(APIStatus.Ok, data=json.loads(json.dumps(data))), HTTPStatus.Ok
