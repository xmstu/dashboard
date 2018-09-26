import time

from flask_restful import abort

from server import log
from server.meta.decorators import make_decorator, Response
from server.meta.session_operation import SessionOperationClass
from server.status import HTTPStatus, make_resp, APIStatus
from server.utils.extend import compare_time, complement_time
from server.utils.role_regions import get_role_regions


class OrdersReceivedStatistics(object):

    @staticmethod
    @make_decorator
    def check_params(params):
        try:
            if not SessionOperationClass.check():
                abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.UnLogin, msg='请登录'))
            params['start_time'] = int(params.get('start_time', None) or time.time() - 86400 * 7)
            params['end_time'] = int(params.get('end_time', None) or time.time())
            params['periods'] = int(params.get('periods', None) or 2)
            params['goods_type'] = int(params.get('goods_type', None) or 0)
            params['goods_price_type'] = int(params.get('goods_price_type', None) or 0)
            params['dimension'] = int(params.get('dimension', None) or 1)
            params['region_id'] = int(params.get('region_id', None) or 0)
            params['comment_type'] = int(params.get('comment_type', None) or 0)
            params['pay_method'] = int(params.get('pay_method', None) or 0)
            params['SXB'] = int(params.get('SXB', None) or 0)

            # 当前权限下所有地区
            params['region_id'] = get_role_regions(params['region_id'])
            # 校验参数
            if not compare_time(params['start_time'], params['end_time']):
                abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='请求时间参数有误'))

            return Response(params=params)
        except Exception as e:
            log.error('Error:{}'.format(e), exc_info=True)
            abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.Forbidden, msg='请求参数有误'))


class CancelOrderReason(object):

    @staticmethod
    @make_decorator
    def check_params(params):
        try:
            if not SessionOperationClass.check():
                abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.UnLogin, msg='请登录'))
            params['start_time'] = int(params.get('start_time', None) or time.time() - 86400 * 7)
            params['end_time'] = int(params.get('end_time', None) or time.time())
            params['goods_type'] = int(params.get('goods_type', None) or 0)
            params['goods_price_type'] = int(params.get('goods_price_type', None) or 0)
            params['cancel_type'] = int(params.get('cancel_type', None) or 1)
            params['region_id'] = int(params.get('region_id', None) or 0)

            # 当前权限下所有地区
            params['region_id'] = get_role_regions(params['region_id'])

            if not compare_time(params['start_time'], params['end_time']):
                abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='请求时间参数有误'))

            return Response(params=params)
        except Exception as e:
            log.error('Error:{}'.format(e), exc_info=True)
            abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.Forbidden, msg='请求参数有误'))


class OrderList(object):

    @staticmethod
    @make_decorator
    def check_params(page, limit, params):
        try:
            if not SessionOperationClass.check():
                abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.UnLogin, msg='请登录'))

            params['order_id'] = int(params.get('order_id', None) or 0)
            params['consignor_mobile'] = int(params.get('consignor_mobile', None) or 0)
            params['driver_mobile'] = int(params.get('driver_mobile', None) or 0)
            params['from_province_id'] = int(params.get('from_province_id', None) or 0)
            params['from_city_id'] = int(params.get('from_city_id', None) or 0)
            params['from_county_id'] = int(params.get('from_county_id', None) or 0)
            params['from_town_id'] = int(params.get('from_town_id', None) or 0)
            params['to_province_id'] = int(params.get('to_province_id', None) or 0)
            params['to_city_id'] = int(params.get('to_city_id', None) or 0)
            params['to_county_id'] = int(params.get('to_county_id', None) or 0)
            params['to_town_id'] = int(params.get('to_town_id', None) or 0)
            params['order_status'] = int(params.get('order_status', None) or 0)
            params['order_type'] = int(params.get('order_type', None) or 0)
            params['order_price_type'] = int(params.get('order_price_type', None) or 0)
            params['vehicle_length'] = str(params.get('vehicle_length', None) or '')
            params['vehicle_type'] = int(params.get('vehicle_type', None) or 0)
            params['region_id'] = int(params.get('node_id', None) or 0)
            params['spec_tag'] = int(params.get('spec_tag', None) or 0)
            params['pay_status'] = int(params.get('pay_status', None) or 0)
            params['is_change_price'] = int(params.get('is_change_price', None) or 0)
            params['comment_type'] = int(params.get('comment_type', None) or 0)
            params['start_order_time'] = int(params.get('start_order_time', None) or time.time() - 86400 * 30)
            params['end_order_time'] = int(params.get('end_order_time', None) or time.time())
            params['start_complete_time'] = int(params.get('start_complete_time', None) or 0)
            params['end_complete_time'] = int(params.get('end_complete_time', None) or 0)
            params['register_start_time'] = int(params.get('register_start_time', None) or 0)
            params['register_end_time'] = int(params.get('register_end_time', None) or 0)
            params['SXB'] = int(params.get('SXB', None) or 0)

            # 补全时间
            params['start_order_time'], params['end_order_time'] = complement_time(params['start_order_time'], params['end_order_time'])
            params['register_start_time'], params['register_end_time'] = complement_time(params['register_start_time'], params['register_end_time'])

            # 当前权限下所有地区
            params['region_id'] = get_role_regions(params['region_id'])

            if not compare_time(params['start_order_time'], params['end_order_time']):
                abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='请求时间参数有误'))

            if not compare_time(params['start_complete_time'], params['end_complete_time']):
                abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='请求时间参数有误'))

            if not compare_time(params['register_start_time'], params['register_end_time']):
                abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='请求时间参数有误'))

            return Response(page=page, limit=limit, params=params)
        except Exception as e:
            log.error('error:{}'.format(e), exc_info=True)
            abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.Forbidden, msg='参数非法'))
