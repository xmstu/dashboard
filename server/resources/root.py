#!/usr/bin/python
# -*- coding:utf-8 -*-
# author=hexm

from flask_restplus.resource import Resource

import server.document.root as doc
from server import api
from server import verify, operations, filters
from server.meta.decorators import Response
from server.meta.session_operation import sessionOperationClass
from server.utils.request import *


class RootManagement(Resource):
    @staticmethod
    @doc.request_root_management_get
    @filters.RootManagement.get_result(params=dict, data=list, before_user_count=int)
    @operations.RootManagement.get_data(params=dict)
    @verify.RootManagement.check_get_params(params=dict)
    def get():
        """获取城市经理或合伙人管理列表"""
        if sessionOperationClass.check():
            role, _ = sessionOperationClass.get_role()
            if role == 1:
                resp = Response(params=get_all_arg())
                return resp
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='仅限后台用户获取消息列表'))
        abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='未登录用户'))

    @staticmethod
    @doc.request_root_management_add
    @operations.RootManagement.post_data(params=dict)
    @verify.RootManagement.check_post_params(params=dict)
    def post():
        """增加新的城市经理或合伙人"""
        if sessionOperationClass.check():
            role, _ = sessionOperationClass.get_role()
            if role == 1:
                resp = Response(params=get_all_arg())
                return resp
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='仅限后台用户获取消息列表'))
        abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='未登录用户'))

    @staticmethod
    @operations.RootManagement.delete_data(params=dict)
    def delete(id):
        """删除该账户"""
        if sessionOperationClass.check():
            role, _ = sessionOperationClass.get_role()
            if role == 1:
                params = get_all_arg()
                params['user_id'] = id
                return Response(params=params)
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='仅限后台用户获取消息列表'))
        abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='未登录用户'))

    @staticmethod
    @doc.request_root_management_put
    @operations.RootManagement.put_data(params=dict)
    @verify.RootManagement.check_put_params(params=dict)
    def put(id):
        """修改当前用户id的账号或者密码"""
        if sessionOperationClass.check():
            role, _ = sessionOperationClass.get_role()
            if role == 1:
                params = get_all_arg()
                params['user_id'] = id
                return Response(params=params)
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='仅限后台用户获取消息列表'))
        abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='未登录用户'))


ns = api.namespace('root', description='超级用户管理')
ns.add_resource(RootManagement, '/management/')
