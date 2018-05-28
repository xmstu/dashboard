# -*- coding: utf-8 -*-

from flask import session
from flask_restplus.resource import Resource

from server import api, verify


class Login(Resource):
    """登录接口"""

    @verify.LoginSetting.post(args=dict)
    def post(self):
        """登录"""
        return {'status': 100000, 'msg': '成功'}


    def delete(self):
        """退出登录"""
        session.pop('login')
        return {'status': 100000, 'msg': '成功'}


ns = api.namespace('login', description='登录接口')
ns.add_resource(Login, '/')
