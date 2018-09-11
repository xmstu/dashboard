import time

from flask_restful import abort

from server import log
from server.meta.decorators import make_decorator, Response
from server.meta.session_operation import SessionOperationClass
from server.status import HTTPStatus, make_result, APIStatus
from server.utils.extend import complement_time, compare_time


class GoodsPotentialDistributionTrend(object):

    @staticmethod
    @make_decorator
    def check_params(params):
        try:
            # 校验有没有登录
            if SessionOperationClass.check():
                role, locations_id = SessionOperationClass.get_locations()
            else:
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.UnLogin, msg='请登录'))

            params['start_time'] = int(params.get('start_time') or time.time() - 86400 * 7)
            params['end_time'] = int(params.get('end_time') or time.time())
            params['periods'] = int(params.get('periods') or 0)
            params['goods_price_type'] = int(params.get('goods_price_type') or 0)
            params['business'] = int(params.get('business') or 1)
            params['haul_dist'] = int(params.get('haul_dist') or 0)
            params['region_id'] = int(params.get('region_id') or 0)

            # 校验地区权限id
            if ('区镇合伙人' in role or '网点管理员' in role or '城市经理' in role) and not str(params['region_id']) in locations_id:
                params['region_id'] = locations_id

            # 补全时间
            params['start_time'], params['end_time'] = complement_time(params['start_time'], params['end_time'])
            # 检测时间正确性
            if not compare_time(params['start_time'], params['end_time']):
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='时间参数非法'))

            return Response(params=params)
        except Exception as e:
            log.error('前端传入参数错误:{}'.format(e))
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.Forbidden, msg='参数非法'))


class GoodsPotentialList(object):

    @staticmethod
    @make_decorator
    def check_params(page, limit, params):
        try:
            # 校验有没有登录
            if SessionOperationClass.check():
                role, locations_id = SessionOperationClass.get_locations()
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
            params['goods_price_type'] = int(params.get('goods_price_type') or 0)
            params['business'] = int(params.get('business') or 1)
            params['haul_dist'] = int(params.get('haul_dist') or 0)
            params['vehicle_length'] = str(params.get('vehicle_length') or 0)
            params['special_tag'] = int(params.get('special_tag') or 0)
            params['register_start_time'] = int(params.get('register_start_time') or 0)
            params['register_end_time'] = int(params.get('register_end_time') or 0)
            params['record_start_time'] = int(params.get('record_start_time') or 0)
            params['record_end_time'] = int(params.get('record_end_time') or 0)
            params['region_id'] = int(params.get('region_id') or 0)

            # 校验权限id
            if ('区镇合伙人' in role or '网点管理员' in role or '城市经理' in role) and not str(params['region_id']) in locations_id:
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
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.Forbidden, msg='参数非法,服务器拒绝该请求'))