# -*- coding: utf-8 -*-

from flask_restful import abort
from flask_restplus import Resource

import server.document.message as doc
from server import operations, api, verify, filters
from server.meta.decorators import Response
from server.meta.session_operation import SessionOperationClass
from server.status import HTTPStatus, make_result, APIStatus
from server.utils.request import get_payload, get_all_arg


class MessageSystem(Resource):
    @staticmethod
    @doc.request_system_message_list_get
    @doc.response_system_message_list_get
    @filters.MessageSystem.get_result(count=int, data=list)
    @operations.MessageSystem.get_message_list(params=dict)
    @verify.MessageSystemVerify.check_get_list_params(params=dict)
    def get():
        """获取消息列表"""
        # 后台用户
        if SessionOperationClass.check():
            role, user_id = SessionOperationClass.get_role()
            if role == '超级管理员':
                resp = Response(params=get_all_arg())
                return resp
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.Forbidden, msg='仅限后台用户获取消息列表'))
        abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.UnLogin, msg='未登录用户'))

    @staticmethod
    @doc.request_system_message_post
    @operations.MessageSystem.post_message(params=dict)
    @verify.MessageSystemVerify.check_post_params(params=dict, user_id=int)
    def post():
        """消息发布"""
        # 后台用户
        if SessionOperationClass.check():
            role, user_id = SessionOperationClass.get_role()
            if role == '超级管理员':
                resp = Response(params=get_payload(), user_id=user_id)
                return resp
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.Forbidden, msg='仅限后台用户发布'))
        abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.UnLogin, msg='未登录用户'))


class MessageSystemOperator(Resource):
    @staticmethod
    @doc.request_system_message_put
    @operations.MessageSystem.put_message(params=dict)
    @verify.MessageSystemVerify.check_put_params(params=dict, user_id=int, msg_id=int)
    def put(id):
        """修改消息内容"""
        # 后台用户
        if SessionOperationClass.check():
            role, user_id = SessionOperationClass.get_role()
            if role == '超级管理员':
                resp = Response(params=get_payload(), user_id=user_id, msg_id=id)
                return resp
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.Forbidden, msg='仅限后台用户修改'))
        abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.UnLogin, msg='未登录用户'))

    @staticmethod
    @operations.MessageSystem.delete_message(params=dict)
    def delete(id):
        """删除消息内容"""
        # 后台用户
        if SessionOperationClass.check():
            role, user_id = SessionOperationClass.get_role()
            if role == '超级管理员':
                resp = Response(params={
                    'user_id': user_id,
                    'msg_id': id
                })
                return resp
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.Forbidden, msg='仅限后台用户删除'))
        abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.UnLogin, msg='未登录用户'))


class MessageUser(Resource):
    @staticmethod
    @doc.request_user_message_list_get
    @doc.response_user_message_list_get
    @filters.MessageUser.get_result(count=int, unread=int, data=list)
    @operations.MessageUser.get_message_list(params=dict)
    @verify.MessageUserVerify.check_get_list_params(params=dict)
    def get():
        """获取消息列表"""
        if not SessionOperationClass.check():
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.UnLogin, msg='未登录用户'))

        resp = Response(params=get_all_arg())
        return resp


class MessageUserOperator(Resource):
    @staticmethod
    @doc.request_user_message_read_get
    @operations.MessageUser.update_msg_read(params=dict)
    @verify.MessageUserVerify.check_is_read_params(params=dict, msg_id=int)
    def get(id):
        """消息已读"""
        if not SessionOperationClass.check():
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.UnLogin, msg='未登录用户'))
        resp = Response(params=get_all_arg(), msg_id=id)
        return resp


ns = api.namespace('message', description='消息窗口接口')
ns.add_resource(MessageSystem, '/system/')
ns.add_resource(MessageSystemOperator, '/system/<int:id>/')
ns.add_resource(MessageUser, '/user/')
ns.add_resource(MessageUserOperator, '/user/<int:id>/')
