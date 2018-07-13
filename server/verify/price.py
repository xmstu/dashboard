import time

from flask_restful import abort

from server import log
from server.meta.decorators import make_decorator, Response
from server.meta.session_operation import sessionOperationClass
from server.status import HTTPStatus, make_result, APIStatus
from server.utils.extend import compare_time


class PriceTrend(object):

    @staticmethod
    @make_decorator
    def check_params(params):
        try:
            params['from_province_id'] = int(params.get('from_province_id') or 0)
            params['from_city_id'] = int(params.get('from_city_id') or 0)
            params['from_county_id'] = int(params.get('from_county_id') or 0)
            params['to_province_id'] = int(params.get('to_province_id') or 0)
            params['to_city_id'] = int(params.get('to_city_id') or 0)
            params['to_county_id'] = int(params.get('to_county_id') or 0)
            params['min_mileage'] = int(params.get('min_mileage') or 0)
            params['max_mileage'] = int(params.get('max_mileage') or 0)
            params['vehicle_length'] = str(params.get('vehicle_length') or '小面包车')
            params['pay_method'] = int(params.get('pay_method') or 0)
            params['start_time'] = int(params.get('start_time') or time.time() - 8*86400)
            params['end_time'] = int(params.get('end_time') or time.time() - 86400)
            params['periods'] = int(params.get('periods') or 1)

            # 当前权限下所有地区
            if sessionOperationClass.check():
                role, locations_id = sessionOperationClass.get_locations()
                if role in (2, 3, 4) and not params.get('region_id'):
                    params['region_id'] = locations_id
                elif role == 1:
                    params['region_id'] = 0
            else:
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='请登录'))

            if not compare_time(params['start_time'], params['end_time']):
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='请求时间参数有误'))

            return Response(params=params)
        except Exception as e:
            log.error('error:{}'.format(e))
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='参数非法'))