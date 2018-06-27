import time

from flask_restful import abort

from server import log
from server.meta.decorators import make_decorator, Response
from server.status import HTTPStatus, make_result, APIStatus
from server.utils.extend import compare_time


class TransportTrend(object):

    @staticmethod
    @make_decorator
    def check_params(params):
        try:
            params['start_time'] = int(params.get('start_time', None) or time.time() - 7 * 86400)
            params['end_time'] = int(params.get('end_time', None) or time.time() - 86400)
            params['periods'] = int(params.get('periods', None) or 2)
            params['region_id'] = int(params.get('region_id', None) or 0)
            params['business'] = int(params.get('business', None) or 0)
            params['vehicle'] = str(params.get('vehicle', None) or '小面包车')

            if not compare_time(params['start_time'], params['end_time']):
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='时间参数有误'))

            return Response(params=params)

        except Exception as e:
            log.error('Error:{}'.format(e))
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='请求参数有误'))
