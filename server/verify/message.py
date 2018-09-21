# -*- coding: utf-8 -*-
import re
from flask_restful import abort
from server import log
from server.meta.decorators import make_decorator, Response
from server.status import HTTPStatus, make_resp, APIStatus


class MessageSystemVerify(object):
    @staticmethod
    @make_decorator
    def check_get_list_params(params):
        try:
            if not params.get('page') or not params['page'].isdigit():
                abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='页数错误'))
            if not params.get('limit') or not params['limit'].isdigit():
                abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='条数错误'))
            params['limit'] = int(params['limit'])
            params['page'] = (int(params['page']) - 1) * params['limit']
            return Response(params=params)
        except Exception as e:
            log.error('Error:{}'.format(e))
            abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='请求参数有误'))

    @staticmethod
    @make_decorator
    def check_post_params(params, user_id):
        try:
            if not params.get('title'):
                abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='标题为空'))
            if not params.get('content'):
                abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='内容为空'))
            if int(params.get('msg_type')) not in [1, 2]:
                abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='消息类型错误'))
            if int(params.get('push_role')) not in [0, 1, 2, 3, 4]:
                abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='推送角色错误'))
            params['content'] = re.sub(r'&nbsp;', '', params['content'])
            params = {
                'user_id': user_id,
                'title': params['title'],
                'content': params['content'],
                'msg_type': int(params['msg_type']),
                'push_role': int(params['push_role'])
            }
            log.debug('消息发布检查参数: [user_id: %s][title: %s][content: %s][msg_type: %s][push_role: %s]'
                      % (
                      params['user_id'], params['title'], params['content'], params['msg_type'], params['push_role']))
            return Response(params=params)
        except Exception as e:
            log.error('Error:{}'.format(e))
            abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='请求参数有误'))

    @staticmethod
    @make_decorator
    def check_put_params(params, user_id, msg_id):
        try:
            if not params.get('title'):
                abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='标题为空'))
            if not params.get('content'):
                abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='内容为空'))
            if params.get('msg_type') not in [1, 2]:
                abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='消息类型错误'))
            if params.get('push_role') not in [0, 1, 2, 3, 4]:
                abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='推送角色错误'))
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
        except Exception as e:
            log.error('Error:{}'.format(e))
            abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='请求参数有误'))


class MessageUserVerify(object):
    @staticmethod
    @make_decorator
    def check_get_list_params(params):
        try:
            params['user_name'] = str(params.get('user_name') or '')
            if not (params.get('user_name') or params.get('account')):
                abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='用户名获取失败'))
            if not params.get('page') or not params['page'].isdigit():
                abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='页数错误'))
            if not params.get('limit') or not params['limit'].isdigit():
                abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='条数错误'))
            params['limit'] = int(params['limit'])
            params['page'] = (int(params['page']) - 1) * params['limit']
            return Response(params=params)
        except Exception as e:
            log.error('Error:{}'.format(e))
            abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='请求参数有误'))

    @staticmethod
    @make_decorator
    def check_is_read_params(params, msg_id):
        try:
            if not params.get('user_name'):
                abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='用户获取失败'))

            params = {
                'account': params['user_name'],
                'msg_id': int(msg_id)
            }
            return Response(params=params)
        except Exception as e:
            log.error('Error:{}'.format(e))
            abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='请求参数有误'))

