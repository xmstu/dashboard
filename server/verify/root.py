from flask_restful import abort

from server import log
from server.meta.decorators import make_decorator, Response
from server.status import HTTPStatus, make_result, APIStatus


class RootManagement(object):

    @staticmethod
    @make_decorator
    def check_get_params(params):
        try:
            if not params.get('page') or not params['page'].isdigit():
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='页数错误'))
            if not params.get('limit') or not params['limit'].isdigit():
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='条数错误'))
            params['page'] = (params['page'] - 1) * params['limit']
            return Response(params=params)
        except Exception as e:
            log.error('error:{}'.format(e))
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='参数非法'))

    @staticmethod
    @make_decorator
    def check_put_params(params):
        try:
            if not params.get('page') or not params['page'].isdigit():
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='页数错误'))
            if not params.get('limit') or not params['limit'].isdigit():
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='条数错误'))

        except Exception as e:
            log.error('error:{}'.format(e))
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='参数非法'))

    @staticmethod
    @make_decorator
    def check_post_params(params):
        try:
            if not params.get('page') or not params['page'].isdigit():
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='页数错误'))
            if not params.get('limit') or not params['limit'].isdigit():
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='条数错误'))

        except Exception as e:
            log.error('error:{}'.format(e))
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='参数非法'))