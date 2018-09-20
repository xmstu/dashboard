# -*- coding: utf-8 -*-

from flask_restplus.resource import Resource

import server.document.login as doc
from server import verify, api, document
from server.utils.request import *
from server.meta.decorators import Response
from server import log, operations, filters
from server.meta.session_operation import SessionOperationClass


@document.response_not_found
@document.response_bad_request
@document.response_internal_server_error
@document.response_unauthorized
class Login(Resource):
    """登录接口"""
    @staticmethod
    @doc.request_user_login
    @doc.response_user_login_success
    @filters.Login.insert_session(result=bool)
    @operations.LoginDecorator.common_check(user_name=str, password=str)
    @verify.LoginSetting.post(user_name=str, password=str)
    def post():
        """用户登录"""
        payload = get_payload()
        user_name = payload.get('user_name', '')
        password = payload.get('password', '')
        resp = Response(user_name=user_name, password=password)

        log.info('获取用户登录请求参数: [user_name: %s][password: %s]' % (resp['user_name'], resp['password']))
        return resp

    @staticmethod
    def delete():
        """用户登出"""
        result = SessionOperationClass.deleted()
        if not result:
            abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='请求参数错误'))
        return {'status': APIStatus.Ok, 'msg': '成功'}, 200


ns = api.namespace('login', description='登录接口')
ns.add_resource(Login, '/')
