from flask_restful import abort
from flask_restplus import Resource

from server import operations, filters, api, document
from server.meta.decorators import Response
from server.meta.session_operation import sessionOperationClass
from server.status import HTTPStatus, make_result, APIStatus


@document.response_not_found
@document.response_bad_request
@document.response_internal_server_error
@document.response_unauthorized
class MessageWindow(Resource):

    @staticmethod
    @filters.MessageWindow.get_result(data=dict)
    @operations.MessageWindow.get_message(params=dict)
    def get():
        """消息窗口"""
        params = {}
        # 当前权限下所有地区
        if sessionOperationClass.check():
            role, locations_id = sessionOperationClass.get_locations()
            if role in (2, 3, 4):
                params['region_id'] = locations_id
        else:
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='请登录'))
        return Response(params=params)


@document.response_not_found
@document.response_bad_request
@document.response_internal_server_error
@document.response_unauthorized
class MessageAll(Resource):

    @staticmethod
    @filters.MessageAll.get_result(data=dict)
    @operations.MessageAll.get_message(params=dict)
    def get():
        """消息窗口"""
        params = {}
        # 当前权限下所有地区
        if sessionOperationClass.check():
            role, locations_id = sessionOperationClass.get_locations()
            if role in (2, 3, 4):
                params['region_id'] = locations_id
        else:
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='请登录'))
        return Response(params=params)


ns = api.namespace('message', description='消息窗口接口')
ns.add_resource(MessageWindow, '/window/')
ns.add_resource(MessageAll, '/all/')
