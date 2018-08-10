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
    @filters.RootManagement.get_result(data=dict)
    @operations.RootManagement.get_data(params=dict)
    @verify.RootManagement.check_get_params(params=dict)
    def get():
        """获取城市经理管理列表"""
        if sessionOperationClass.check():
            role, _ = sessionOperationClass.get_role()
            if role == 1:
                resp = Response(params=get_all_arg())
                return resp
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='仅限后台用户获取账户列表'))
        abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='未登录用户'))

    @staticmethod
    @doc.request_root_management_add
    @operations.RootManagement.post_data(params=dict)
    @verify.RootManagement.check_post_params(params=dict)
    def post():
        """增加新的城市经理"""
        if sessionOperationClass.check():
            role, supper_user_id = sessionOperationClass.get_role()
            if role == 1 and supper_user_id == 322:
                resp = Response(params=get_payload())
                return resp
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='仅限超级管理员添加账户'))
        abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='未登录用户'))


class RootManagementOperator(Resource):
    @staticmethod
    @operations.RootManagement.delete_data(params=dict)
    def delete(user_id):
        """删除该账户"""
        if sessionOperationClass.check():
            role, supper_user_id = sessionOperationClass.get_role()
            if role == 1 and supper_user_id == 322:
                return Response(params={'user_id': user_id})
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='仅限超级管理员删除账户'))
        abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='未登录用户'))

    @staticmethod
    @doc.request_root_management_put
    @operations.RootManagement.put_data(params=dict)
    @verify.RootManagement.check_put_params(params=dict)
    def put(user_id):
        """修改当前用户id的账号或者密码"""
        if sessionOperationClass.check():
            role, supper_user_id = sessionOperationClass.get_role()
            if role == 1 and supper_user_id == 322:
                if user_id == 0:
                    abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='用户id不能为0'))
                params = get_payload()
                params.setdefault('user_id', user_id)
                return Response(params=params)
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='仅限超级管理员修改账户'))
        abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='未登录用户'))


ns = api.namespace('root', description='城市经理管理')
ns.add_resource(RootManagement, '/management/')
ns.add_resource(RootManagementOperator, '/management/<int:user_id>')
