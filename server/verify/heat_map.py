from flask_restful import abort

from server import log
from server.meta.decorators import make_decorator
from server.status import HTTPStatus, make_result, APIStatus


class HeatMap(object):

    @staticmethod
    @make_decorator
    def check_params(params):
        try:
            pass
        except Exception as e:
            log.error('error:{}'.format(e))
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='参数非法'))