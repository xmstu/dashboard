from flask_restful import abort

from server import log
from server.meta.decorators import make_decorator, Response
from server.meta.session_operation import sessionOperationClass
from server.status import HTTPStatus, make_result, APIStatus
from server.utils.extend import complement_time, compare_time


class GoodsPotentialDistributionTrend(object):

    @staticmethod
    @make_decorator
    def check_params(params, **kwargs):
        try:
            pass
        except Exception as e:
            log.error('error:{}'.format(e))
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='参数非法'))


class GoodsPotentialList(object):

    @staticmethod
    @make_decorator
    def check_params(page, limit, params):
        try:
            # 校验有没有登录
            if sessionOperationClass.check():
                role, locations_id = sessionOperationClass.get_locations()
                if role == 1:
                    locations_id = None
            else:
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.UnLogin, msg='请登录'))

            params['from_province_id'] = int(params.get('from_province_id') or 0)
            params['from_city_id'] = int(params.get('from_city_id') or 0)
            params['from_county_id'] = int(params.get('from_county_id') or 0)
            params['from_town_id'] = int(params.get('from_town_id') or 0)
            params['to_province_id'] = int(params.get('to_province_id') or 0)
            params['to_city_id'] = int(params.get('to_city_id') or 0)
            params['to_county_id'] = int(params.get('to_county_id') or 0)
            params['to_town_id'] = int(params.get('to_town_id') or 0)
            params['goods_type'] = int(params.get('goods_type') or 0)
            params['business'] = int(params.get('business') or 1)
            params['vehicle_length'] = str(params.get('vehicle_length') or 0)
            params['special_tag'] = int(params.get('special_tag') or 0)
            params['register_start_time'] = int(params.get('register_start_time') or 0)
            params['register_end_time'] = int(params.get('register_end_time') or 0)
            params['record_start_time'] = int(params.get('record_start_time') or 0)
            params['record_end_time'] = int(params.get('record_end_time') or 0)
            params['region_id'] = locations_id
            # 补全时间
            params['register_start_time'], params['register_end_time'] = complement_time(params['register_start_time'], params['register_end_time'])
            params['record_start_time'], params['record_end_time'] = complement_time(params['record_start_time'], params['record_end_time'])
            # 检测时间正确性
            if not compare_time(params['register_start_time'], params['register_end_time']):
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='时间参数非法'))
            if not compare_time(params['record_start_time'], params['record_end_time']):
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='时间参数非法'))

            return Response(params=params, page=page, limit=limit)
        except Exception as e:
            log.error('前端传入参数错误:{}'.format(e))
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='参数非法'))