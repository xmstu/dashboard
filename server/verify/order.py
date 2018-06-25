import time

from flask_restful import abort

from server import log
from server.meta.decorators import make_decorator, Response
from server.meta.session_operation import sessionOperationClass
from server.status import HTTPStatus, make_result, APIStatus


class OrdersReceivedStatistics(object):

    @staticmethod
    @make_decorator
    def check_params(params):
        try:
            params['start_time'] = int(params.get('start_time', None) or time.time() - 86400 * 8)
            params['end_time'] = int(params.get('end_time', None) or time.time() - 86400)
            params['periods'] = int(params.get('periods', None) or 2)
            params['goods_type'] = int(params.get('goods_type', None) or 0)
            params['dimension'] = int(params.get('dimension', None) or 1)
            params['region_id'] = int(params.get('region_id', None) or 0)
            params['comment_type'] = int(params.get('comment_type', None) or 0)
            params['pay_method'] = int(params.get('pay_method', None) or 0)

            if params['start_time'] <= params['end_time'] < time.time():
                pass
            else:
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='请求时间参数有误'))

            return Response(params=params)
        except Exception as e:
            log.error('Error:{}'.format(e))
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='请求参数有误'))


class CancelOrderReason(object):

    @staticmethod
    @make_decorator
    def check_params(params):
        try:
            params['start_time'] = int(params.get('start_time', None) or time.time() - 86400 * 7)
            params['end_time'] = int(params.get('end_time', None) or time.time() - 86400)
            params['goods_type'] = int(params.get('goods_type', None) or 0)
            params['cancel_type'] = int(params.get('cancel_type',None) or 1)
            params['region_id'] = int(params.get('region_id', None) or 0)

            if params['start_time'] <= params['end_time'] < time.time():
                pass
            else:
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='请求时间参数有误'))

            return Response(params=params)
        except Exception as e:
            log.error('Error:{}'.format(e))
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='请求参数有误'))


class OrderList(object):

    @staticmethod
    @make_decorator
    def check_params(page, limit, params):
        try:
            params['order_id'] = int(params.get('order_id', None) or 0)
            params['consignor_mobile'] = int(params.get('consignor_mobile', None) or 0)
            params['driver_mobile'] = int(params.get('driver_mobile', None) or 0)
            params['from_province_id'] = int(params.get('from', None) or 0)
            params['from_city_id'] = int(params.get('from', None) or 0)
            params['from_county_id'] = int(params.get('from', None) or 0)
            params['to_province_id'] = int(params.get('to', None) or 0)
            params['to_city_id'] = int(params.get('to', None) or 0)
            params['to_county_id'] = int(params.get('to', None) or 0)
            params['order_status'] = int(params.get('order_status', None) or 0)
            params['order_type'] = int(params.get('order_type', None) or 0)
            params['vehicle_length'] = int(params.get('vehicle_length', None) or 0)
            params['vehicle_type'] = int(params.get('vehicle_type', None) or 0)
            params['node_id'] = int(params.get('node_id', None) or 0)
            params['spec_tag'] = int(params.get('spec_tag', None) or 0)
            params['pay_status'] = int(params.get('pay_status', None) or 0)
            params['is_change_price'] = int(params.get('is_change_price', None) or 0)
            params['comment_type'] = int(params.get('comment_type', None) or 0)
            params['start_order_time'] = int(params.get('start_order_time', None) or time.time() - 86400 * 7)
            params['end_order_time'] = int(params.get('end_order_time', None) or time.time() - 86400)
            params['start_loading_time'] = int(params.get('start_loading_time', None) or time.time() - 86400 * 7)
            params['end_loading_time'] = int(params.get('end_loading_time', None) or time.time() - 86400)

            # 当前权限下所有地区
            if sessionOperationClass.check():
                role, locations_id = sessionOperationClass.get_locations()
                if role in (2, 3, 4) and not params['node_id']:
                    params['node_id'] = locations_id
            else:
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='请登录'))

            if params['start_order_time'] <= params['end_order_time'] < time.time():
                pass
            else:
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='请求时间参数有误'))

            if params['start_loading_time'] <= params['end_loading_time'] < time.time():
                pass
            else:
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='请求时间参数有误'))

            return Response(page=page, limit=limit, params=params)
        except Exception as e:
            log.error('error:{}'.format(e))
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='参数非法'))