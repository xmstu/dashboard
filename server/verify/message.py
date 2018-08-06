# -*- coding: utf-8 -*-

from flask_restful import abort

from server import log
from server.meta.decorators import make_decorator, Response
from server.status import HTTPStatus, make_result, APIStatus


class MessageSystemVerify(object):
    @staticmethod
    @make_decorator
    def check_get_list_params(params):
        if not params.get('page') or not params['page'].isdigit():
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='页数错误'))
        if not params.get('limit') or not params['limit'].isdigit():
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='条数错误'))
        params['limit'] = int(params['limit'])
        params['page'] = (int(params['page']) - 1) * params['limit']
        return Response(params=params)

    @staticmethod
    @make_decorator
    def check_post_params(params, user_id):
        if not params.get('title'):
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='标题为空'))
        if not params.get('content'):
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='内容为空'))
        if int(params.get('msg_type')) not in [1,2]:
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='消息类型错误'))
        if int(params.get('push_role')) not in [0,1,2,3,4]:
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='推送角色错误'))
        params = {
            'user_id': user_id,
            'title': params['title'],
            'content': params['content'],
            'msg_type': int(params['msg_type']),
            'push_role': int(params['push_role'])
        }
        log.debug('消息发布检查参数: [user_id: %s][title: %s][content: %s][msg_type: %s][push_role: %s]'
                  % (params['user_id'], params['title'], params['content'], params['msg_type'], params['push_role']))
        return Response(params=params)

    @staticmethod
    @make_decorator
    def check_put_params(params, user_id, msg_id):
        if not params.get('title'):
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='标题为空'))
        if not params.get('content'):
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='内容为空'))
        if params.get('msg_type') not in [1, 2]:
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='消息类型错误'))
        if params.get('push_role') not in [0, 1, 2, 3, 4]:
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='推送角色错误'))
        params = {
            'user_id': user_id,
            'msg_id': msg_id,
            'title': params['title'],
            'content': params['content'],
            'msg_type': params['msg_type'],
            'push_role': params['push_role']
        }
        log.debug('消息修改检查参数: [user_id: %s][msg_id: %s][title: %s][content: %s][msg_type: %s][push_role: %s]'
                  % (params['user_id'], params['msg_id'], params['title'], params['content'], params['msg_type'],
                     params['push_role']))
        return Response(params=params)


class MessageUserVerify(object):
    @staticmethod
    @make_decorator
    def check_get_list_params(params):
        if not params.get('account'):
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='用户获取失败'))
        if not params.get('page') or not params['page'].isdigit():
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='页数错误'))
        if not params.get('limit') or not params['limit'].isdigit():
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='条数错误'))
        params['limit'] = int(params['limit'])
        params['page'] = (int(params['page']) - 1) * params['limit']
        return Response(params=params)

    @staticmethod
    @make_decorator
    def check_is_read_params(params, msg_id):
        if not params.get('account'):
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='用户获取失败'))

        params = {
            'account': params['account'],
            'msg_id': msg_id
        }
        return Response(params=params)
