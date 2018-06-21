# -*- coding: utf-8 -*-
from flask import session
from flask_restplus.resource import Resource

import server.document.login as doc
from server import verify, api, document
from server.utils.request import *
from server.meta.decorators import Response
from server import log, operations, filters


@document.response_not_found
@document.response_bad_request
@document.response_internal_server_error
@document.response_unauthorized
class Login(Resource):
    """登录接口"""
    @staticmethod
    @doc.request_user_login
    @doc.response_user_login_success
    @filters.Login.insert_session(user_info=dict, role=int, locations=list)
    @operations.LoginDecorator.common_check(user_name=str, password=str, role=int)
    @verify.LoginSetting.post(user_name=str, password=str, role=int)
    def post():
        """用户登录"""
        user_name = get_arg('user_name', '')
        password = get_arg('password', '')
        role = get_arg_int('role', 1)
        resp = Response(user_name=user_name, password=password, role=role)

        log.info('获取用户登录请求参数: [user_name: %s][password: %s][resp: %s]' % (resp['user_name'], resp['password'], resp['role']))
        return resp

    @staticmethod
    def delete():
        """用户登出"""
        if not session.get('login'):
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='请求参数错误'))
        del session['login']
        return {'status': APIStatus.Ok, 'msg': '成功'}, 200


ns = api.namespace('login', description='登录接口')
ns.add_resource(Login, '/')
