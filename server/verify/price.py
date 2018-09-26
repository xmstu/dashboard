import time

from flask_restful import abort

from server import log
from server.meta.decorators import make_decorator, Response
from server.meta.session_operation import SessionOperationClass
from server.status import HTTPStatus, make_resp, APIStatus
from server.utils.extend import compare_time
from server.utils.role_regions import get_role_regions


class PriceTrend(object):

    @staticmethod
    @make_decorator
    def check_params(params):
        try:
            if not SessionOperationClass.check():
                abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.UnLogin, msg='请登录'))
            params['from_province_id'] = int(params.get('from_province_id') or 0)
            params['from_city_id'] = int(params.get('from_city_id') or 0)
            params['from_county_id'] = int(params.get('from_county_id') or 0)
            params['to_province_id'] = int(params.get('to_province_id') or 0)
            params['to_city_id'] = int(params.get('to_city_id') or 0)
            params['to_county_id'] = int(params.get('to_county_id') or 0)
            params['min_mileage'] = int(params.get('min_mileage') or 0)
            params['max_mileage'] = int(params.get('max_mileage') or 0)
            params['vehicle_length'] = str(params.get('vehicle_length') or '小面包车')
            params['order_status'] = int(params.get('order_status') or 0)
            params['start_time'] = int(params.get('start_time') or time.time() - 90*86400)
            params['end_time'] = int(params.get('end_time') or time.time())

            # 当前权限下所有地区
            params['region_id'] = get_role_regions(int(params.get('region_id') or 0))

            if not compare_time(params['start_time'], params['end_time']):
                abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='请求时间参数有误'))

            return Response(params=params)
        except Exception as e:
            log.error('error:{}'.format(e))
            abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.Forbidden, msg='拒绝请求'))