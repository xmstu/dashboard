#!/usr/bin/python
# -*- coding:utf-8 -*-
# author=hexm

from flask import session, abort
from flask_restplus.resource import Resource

from server import api
from server.meta.session_operation import sessionOperationClass
from server.status import HTTPStatus, make_result, APIStatus


class RoleChange(Resource):

    @staticmethod
    def get():
        if sessionOperationClass.check():
            return make_result(APIStatus.Ok, data=sessionOperationClass.get_session('user_session')), HTTPStatus.Ok


class RoleChangeOperator(Resource):
    @staticmethod
    def put(role_id):
        if not sessionOperationClass.check():
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='必须登录才能切换角色!'))
        if not isinstance(role_id, int):
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='角色id必须是整数'))
        for role_info in session['user_session']:
            if role_id == role_info['role_id']:
                login = sessionOperationClass.get_session('login')
                # 先清空login信息
                if not sessionOperationClass.deleted():
                    abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='请求参数错误'))
                # 再切换角色信息
                if sessionOperationClass.change_role(login, role_info):
                    return make_result(APIStatus.Ok, msg="角色切换成功"), HTTPStatus.Ok
                else:
                    return make_result(APIStatus.InternalServerError, msg="角色切换失败"), HTTPStatus.InternalServerError


ns = api.namespace('role_change', description='角色切换')
ns.add_resource(RoleChange, '/role_change/')
ns.add_resource(RoleChangeOperator, '/role_change/<int:role_id>')
