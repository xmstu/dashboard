#!/usr/bin/python
# -*- coding:utf-8 -*-
# author=hexm
from flask import session

from server.meta.decorators import make_decorator
from server.status import UserAPIStatus
from server.status.message import direct_response


class Login(object):

    @staticmethod
    @make_decorator
    def post(args):
        session['login'] = {
            'user_id': args.get('user_id'),
            'mobile': args.get('mobile'),
        }
        return direct_response({'status': UserAPIStatus.Ok, 'msg': '登录成功'})
