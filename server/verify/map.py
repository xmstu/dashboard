import time

from flask_restful import abort

from server import log
from server.meta.decorators import make_decorator, Response
from server.meta.session_operation import SessionOperationClass
from server.status import HTTPStatus, make_resp, APIStatus
from server.utils.extend import compare_time, check_region_id, date2timestamp, timestamp2date, complement_time
from server.utils.role_regions import get_role_regions

today_begin = date2timestamp(timestamp2date(time.time()))


class DistributionMap(object):

    @staticmethod
    @make_decorator
    def check_params(params):
        try:
            if not SessionOperationClass.check():
                abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.UnLogin, msg='请登录'))

            params['dimension'] = int(params.get('dimension', None) or 1)
            params['filter'] = params.get('filter', None) or 0
            params['field'] = int(params.get('field', None) or 1)
            params['start_time'] = int(params.get('start_time', None) or time.time() - 86400 * 7)
            params['end_time'] = int(params.get('end_time', None) or time.time())
            params['region_id'] = str(params.get('region_id', None) or '0')

            role_type, locations_id = SessionOperationClass.get_locations()
            # 校验权限id
            if 4 == role_type:
                params['role_region_id'] = locations_id
                params['authority_region_id'] = locations_id[0]
                params['region_id'] = params['region_id'] if params['region_id'] != '0' else params[
                    'authority_region_id']
            elif role_type == 1:
                params['role_region_id'] = locations_id + ['0']
            else:
                params['role_region_id'] = ''

            if not check_region_id(params['region_id'], params['role_region_id']):
                abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='地区参数非法'))

            if not compare_time(params['start_time'], params['end_time']):
                abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='时间参数非法'))

            return Response(params=params)
        except Exception as e:
            log.error('校验分布地图参数失败:{}'.format(e), exc_info=True)
            abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.Forbidden, msg='拒绝请求'))


class GoodsMap(object):

    @staticmethod
    @make_decorator
    def check_params(params):
        try:
            if not SessionOperationClass.check():
                abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.UnLogin, msg='请登录'))

            params['goods_price_type'] = int(params.get('goods_price_type', None) or 0)
            params['haul_dist'] = int(params.get('haul_dist', None) or 0)
            params['vehicle_length'] = str(params.get('vehicle_length', None) or '')
            params['goods_status'] = int(params.get('goods_status', None) or 0)
            params['special_tag'] = int(params.get('special_tag', None) or 0)
            params['delivery_start_time'] = int(params.get('delivery_start_time', None) or today_begin)
            params['delivery_end_time'] = int(params.get('delivery_end_time', None) or time.time())
            params['register_start_time'] = int(params.get('register_start_time', None) or 0)
            params['register_end_time'] = int(params.get('register_end_time', None) or 0)

            # 补全时间
            params['delivery_start_time'], params['delivery_end_time'] = complement_time(params['delivery_start_time'],
                                                                                         params['delivery_end_time'])
            params['register_start_time'], params['register_end_time'] = complement_time(params['register_start_time'],
                                                                                         params['register_end_time'])

            if not compare_time(params['delivery_start_time'], params['delivery_end_time']):
                abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='时间参数非法'))

            if not compare_time(params['register_start_time'], params['register_end_time']):
                abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='时间参数非法'))

            return Response(params=params)
        except Exception as e:
            log.error('校验货源热图参数失败:{}'.format(e), exc_info=True)
            abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.Forbidden, msg='拒绝请求'))


class UsersMap(object):

    @staticmethod
    @make_decorator
    def check_params(params):
        try:
            if not SessionOperationClass.check():
                abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.UnLogin, msg='请登录'))

            params['users_type'] = int(params.get('users_type') or 0)
            params['is_auth'] = int(params.get('is_auth') or 0)
            params['active_level'] = int(params.get('active_level') or 0)
            params['special_tag'] = int(params.get('special_tag') or 0)
            params['register_start_time'] = int(params.get('register_start_time') or today_begin)
            params['register_end_time'] = int(params.get('register_end_time') or time.time())
            params['position_start_time'] = int(params.get('position_start_time') or today_begin)
            params['position_end_time'] = int(params.get('position_end_time') or time.time())

            # 补全时间
            params['register_start_time'], params['register_end_time'] = complement_time(params['register_start_time'],
                                                                                         params['register_end_time'])
            params['position_start_time'], params['position_end_time'] = complement_time(params['position_start_time'],
                                                                                         params['position_end_time'])

            # 获取权限地区id
            params['role_region_id'] = get_role_regions(0)

            if not compare_time(params['register_start_time'], params['register_end_time']):
                abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='时间参数非法'))

            if not compare_time(params['position_start_time'], params['position_end_time']):
                abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='时间参数非法'))

            return Response(params=params)
        except Exception as e:
            log.error('校验用户热图参数失败:{}'.format(e))
            abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='参数非法'))
