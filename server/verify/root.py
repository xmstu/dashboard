import hashlib

from flask_restful import abort

from server import log
from server.meta.decorators import make_decorator, Response
from server.status import HTTPStatus, make_result, APIStatus
from server.utils.extend import pwd_to_hash


class RootManagement(object):

    @staticmethod
    @make_decorator
    def check_get_params(params):
        try:
            if not params.get('page') or not params['page'].isdigit():
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='页数错误'))
            if not params.get('limit') or not params['limit'].isdigit():
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='条数错误'))
            params['page'], params['limit'] = (int(params['page']) - 1) * int(params['limit']), int(params['limit'])
            return Response(params=params)
        except Exception as e:
            log.error('error:{}'.format(e))
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='参数非法'))

    @staticmethod
    @make_decorator
    def check_put_params(params):
        try:
            params['account'] = str(params.get('account') or '')
            params['user_name'] = str(params.get('user_name') or '')
            params['password'] = pwd = str(params.get('password') or '')
            params['region_id'] = int(params.get('region_id') or 0)
            params['user_id'] = int(params.get('user_id') or 0)
            # 加密密码
            params['password'] = pwd_to_hash(pwd)
            return Response(params=params)
        except Exception as e:
            log.error('error:{}'.format(e))
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='参数非法'))

    @staticmethod
    @make_decorator
    def check_post_params(params):
        try:
            params['account'] = str(params.get('account') or '')
            params['user_name'] = str(params.get('user_name') or '')
            params['password'] = pwd = str(params.get('password') or '')
            params['region_id'] = int(params.get('region_id') or 0)

            # 加密密码
            params['password'] = pwd_to_hash(pwd)

            return Response(params=params)
        except Exception as e:
            log.error('error:{}'.format(e))
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='参数非法'))