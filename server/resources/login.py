# -*- coding: utf-8 -*-
import logging

from flask import session, request
from flask_restplus.resource import Resource

from server import api, verify, log, operations, filters
from server.workflow.passing import Passing
from server.workflow.utils import performance


class Login(Resource):
    """登录接口"""

    # @document.request_os_header
    # @document.request_devel_header
    # @doc.api_user_register_doc
    # @doc.response_user_login_success
    @performance(log=log, level=logging.INFO)
    # @collect_exceptions(message_handler)
    @filters.Login.post(args=dict)
    @operations.LoginDecorator.post(args=dict)
    @operations.LoginDecorator.common_check(args=dict)
    @verify.LoginSetting.post(args=dict)
    def post(self):
        """用户登录"""
        args = request.get_json()
        log.info('login %s' % args)
        return Passing(args=args)


    def delete(self):
        """退出登录"""
        session.pop('login')
        return {'status': 100000, 'msg': '成功'}


ns = api.namespace('login', description='登录接口')
ns.add_resource(Login, '/')
