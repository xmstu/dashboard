import time

from flask_restful import abort

from server import log
from server.meta.decorators import make_decorator, Response
from server.meta.session_operation import SessionOperationClass
from server.status import HTTPStatus, make_result, APIStatus
from server.utils.extend import compare_time
from server.utils.role_regions import get_role_regions


class TransportRadar(object):

    @staticmethod
    @make_decorator
    def check_params(params):
        try:
            if not SessionOperationClass.check():
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='请登录'))
            params['start_time'] = int(params.get('start_time', None) or time.time() - 7 * 86400)
            params['end_time'] = int(params.get('end_time', None) or time.time() - 86400)
            params['region_id'] = int(params.get('region_id', None) or 0)
            params['from_province_id'] = int(params.get('from_province_id', None) or 0)
            params['from_city_id'] = int(params.get('from_city_id', None) or 0)
            params['from_county_id'] = int(params.get('from_county_id', None) or 0)
            params['from_town_id'] = int(params.get('from_town_id', None) or 0)
            params['to_province_id'] = int(params.get('to_province_id', None) or 0)
            params['to_city_id'] = int(params.get('to_city_id', None) or 0)
            params['to_county_id'] = int(params.get('to_county_id', None) or 0)
            params['to_town_id'] = int(params.get('to_town_id', None) or 0)

            # 当前权限下所有地区
            params['region_id'] = get_role_regions(params['region_id'])

            if not compare_time(params['start_time'], params['end_time']):
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='时间参数有误'))

            return Response(params=params)

        except Exception as e:
            log.error('Error:{}'.format(e), exc_info=True)
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='请求参数有误'))


class TransportList(object):

    @staticmethod
    @make_decorator
    def check_params(page, limit, params):
        try:
            if not SessionOperationClass.check():
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='请登录'))
            # 校验参数并赋予默认值
            params['from_province_id'] = int(params.get('from_province_id', None) or 0)
            params['from_city_id'] = int(params.get('from_city_id', None) or 0)
            params['from_county_id'] = int(params.get('from_county_id', None) or 0)
            params['to_province_id'] = int(params.get('to_province_id', None) or 0)
            params['to_city_id'] = int(params.get('to_city_id', None) or 0)
            params['to_county_id'] = int(params.get('to_county_id', None) or 0)
            params['vehicle_length'] = str(params.get('vehicle_length', None) or '')
            params['start_time'] = int(params.get('start_time', None) or time.time() - 86400 * 7)
            params['end_time'] = int(params.get('end_time', None) or time.time() - 86400)
            params['region_id'] = int(params['region_id'] or 0)

            params['region_id'] = get_role_regions(params['region_id'])
            # 校验时间
            if not compare_time(params['start_time'], params['end_time']):
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='筛选时间参数有误'))

            return Response(page=page, limit=limit, params=params)

        except Exception as e:
            log.error('error:{}'.format(e), exc_info=True)
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='参数非法'))
