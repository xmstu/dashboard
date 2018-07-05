import time

from flask_restful import abort

from server import log
from server.meta.decorators import make_decorator
from server.status import HTTPStatus, make_result, APIStatus


class HeatMap(object):

    @staticmethod
    @make_decorator
    def check_params(params):
        try:
            params['dimension'] = int(params.get('dimension', None) or 1)
            params['filter'] = int(params.get('filter', None) or 1)
            params['field'] = int(params.get('field', None) or 1)
            params['start_time'] = int(params.get('start_time', None) or time.time() - 86400*7)
            params['end_time'] = int(params.get('end_time', None) or time.time())

        except Exception as e:
            log.error('error:{}'.format(e))
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='参数非法'))