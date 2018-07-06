import time

from flask_restful import abort

from server import log
from server.meta.decorators import make_decorator
from server.meta.session_operation import sessionOperationClass
from server.status import HTTPStatus, make_result, APIStatus
from server.utils.extend import compare_time


class HeatMap(object):

    @staticmethod
    @make_decorator
    def check_params(params):
        try:
            # 当前权限下所有地区
            if sessionOperationClass.check():
                role, locations_id = sessionOperationClass.get_locations()
                if role in (2, 3, 4) and not params.get('region_id'):
                    params['region_id'] = locations_id
            else:
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='请登录'))

            params['dimension'] = int(params.get('dimension', None) or 1)
            params['filter'] = int(params.get('filter', None) or 1)
            params['field'] = int(params.get('field', None) or 0)
            params['start_time'] = int(params.get('start_time', None) or time.time() - 86400*7)
            params['end_time'] = int(params.get('end_time', None) or time.time())
            params['region_name'] = int(params.get('end_time', None) or time.time())

            if not compare_time(params['start_time'], params['end_time']):
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='时间参数非法'))

        except Exception as e:
            log.error('error:{}'.format(e), exc_info=True)
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='参数非法'))