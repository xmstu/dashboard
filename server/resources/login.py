# -*- coding: utf-8 -*-
import logging

from flask import session, request
from flask_restplus.resource import Resource

import server.document.login as doc
from server import api, verify, log, operations, filters
from server.status import UserAPIStatus
from server.status.message import message_handler, direct_response
from server.workflow.passing import Passing
from server.workflow.utils import performance, collect_exceptions
from server.utils.request import *


class Login(Resource):
    """登录接口"""

    @doc.api_user_register_doc
    @doc.response_user_login_success
    @performance(log=log, level=logging.INFO)
    @collect_exceptions(message_handler)
    @filters.Login.post(args=dict)
    @operations.LoginDecorator.common_check(args=dict)
    @verify.LoginSetting.post(args=dict)
    def post(self):
        """用户登录"""
        args = get_payload()
        log.info('login %s' % args)
        return Passing(args=args)

    @staticmethod
    def delete():
        """用户登出"""
        if not session.get('login'):
            return direct_response({'status': UserAPIStatus.Ok, 'msg': '成功'})
        del session['login']
        return direct_response({'status': UserAPIStatus.Ok, 'msg': '成功'})


ns = api.namespace('login', description='登录接口')
ns.add_resource(Login, '/')
