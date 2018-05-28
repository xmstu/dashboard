#!/usr/bin/python
# -*- coding:utf-8 -*-
# author=hexm
import time

from flask import session

from server.status import UserAPIStatus
from server.status.message import direct_response
from server.workflow.passing import make_passing


class Login(object):

    @staticmethod
    @make_passing
    def post(args):
        session['login'] = {
            'user_id': args['user_id'],
            'mobile': args['mobile'],
            'login_time': time.time()
        }
        return direct_response({'status': UserAPIStatus.Ok, 'msg': '登录成功'})
