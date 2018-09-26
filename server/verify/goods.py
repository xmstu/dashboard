import time

from flask_restful import abort

from server import log
from server.meta.decorators import make_decorator, Response
from server.meta.session_operation import SessionOperationClass
from server.status import HTTPStatus, make_resp, APIStatus
from server.utils.extend import compare_time, complement_time
from server.utils.role_regions import get_role_regions


class GoodsList(object):

    @staticmethod
    @make_decorator
    def check_params(page, limit, params):
        try:
            if not SessionOperationClass.check():
                abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.UnLogin, msg='请登录'))

            params['create_start_time'] = int(params.get('create_start_time') or time.time() - 86400 * 30)
            params['create_end_time'] = int(params.get('create_end_time') or time.time())
            params['register_start_time'] = int(params.get('register_start_time') or 0)
            params['register_end_time'] = int(params.get('register_end_time') or 0)
            params['goods_id'] = int(params.get('goods_id') or 0)
            params['mobile'] = int(params.get('mobile') or 0)
            params['from_province_id'] = int(params.get('from_province_id') or 0)
            params['from_city_id'] = int(params.get('from_city_id') or 0)
            params['from_county_id'] = int(params.get('from_county_id') or 0)
            params['from_town_id'] = int(params.get('from_town_id') or 0)
            params['to_province_id'] = int(params.get('to_province_id') or 0)
            params['to_city_id'] = int(params.get('to_city_id') or 0)
            params['to_county_id'] = int(params.get('to_county_id') or 0)
            params['to_town_id'] = int(params.get('to_town_id') or 0)
            params['goods_type'] = int(params.get('goods_type') or 0)
            params['goods_price_type'] = int(params.get('goods_price_type') or 0)
            params['goods_status'] = int(params.get('goods_status') or 0)
            params['is_called'] = int(params.get('is_called') or 0)
            params['vehicle_length'] = int(params.get('vehicle_length') or 0)
            params['vehicle_type'] = int(params.get('vehicle_type') or 0)
            params['region_id'] = int(params.get('node_id') or 0)
            params['new_goods_type'] = int(params.get('new_goods_type') or 0)
            params['urgent_goods'] = int(params.get('urgent_goods') or 0)
            params['is_addition'] = int(params.get('is_addition') or 0)
            params['payment_method'] = int(params.get('payment_method') or 0)

            # 当前权限下所有地区
            params['region_id'] = get_role_regions(params['region_id'])

            # 补全时间
            params['create_start_time'], params['create_end_time'] = complement_time(params['create_start_time'], params['create_end_time'])
            # 校验参数
            if not compare_time(params['create_start_time'], params['create_end_time']):
                abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='时间参数有误'))
            if not compare_time(params['register_start_time'], params['register_end_time']):
                abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='时间参数有误'))

            log.debug("货源列表验证参数{}".format(params))
            return Response(page=page, limit=limit, params=params)

        except Exception as e:
            log.error('Error:{}'.format(e), exc_info=True)
            abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.Forbidden, msg='请求参数有误'))


class CancelGoodsReason(object):

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
            params['region_id'] = int(params.get('region_id', None) or 0)

            # 当前权限下所有地区
            params['region_id'] = get_role_regions(params['region_id'])
            # 补全时间
            params['start_time'], params['end_time'] = complement_time(params['start_time'], params['end_time'])
            # 校验时间
            if not compare_time(params['start_time'], params['end_time']):
                abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='时间参数有误'))

            return Response(params=params)
        except Exception as e:
            log.error('Error:{}'.format(e), exc_info=True)
            abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.Forbidden, msg='请求参数有误'))


class GoodsDistributionTrend(object):

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
            params['region_id'] = int(params.get('region_id', None) or 0)
            params['payment_method'] = int(params.get('payment_method', None) or 0)

            # 当前权限下所有地区
            params['region_id'] = get_role_regions(params['region_id'])
            # 补全时间
            params['start_time'], params['end_time'] = complement_time(params['start_time'], params['end_time'])
            # 校验时间
            if not compare_time(params['start_time'], params['end_time']):
                abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='时间参数有误'))

            return Response(params=params)
        except Exception as e:
            log.error('Error:{}'.format(e), exc_info=True)
            abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.Forbidden, msg='请求参数有误'))
