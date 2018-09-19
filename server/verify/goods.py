import time

from flask_restful import abort

from server import log
from server.meta.decorators import make_decorator, Response
from server.meta.session_operation import SessionOperationClass
from server.status import HTTPStatus, make_result, APIStatus
from server.utils.extend import compare_time, complement_time


class GoodsList(object):

    @staticmethod
    @make_decorator
    def check_params(page, limit, params):
        # 通过params获取参数
        try:
            create_start_time = int(params.get('create_start_time')) if params.get(
                'create_start_time') else time.time() - 86400 * 7
            create_end_time = int(params.get('create_end_time')) if params.get('create_end_time') else time.time()
            register_start_time = int(params.get('register_start_time', None) or 0)
            register_end_time = int(params.get('register_end_time', None) or 0)

            goods_id = params.get('goods_id') if params.get('goods_id') else ''
            mobile = params.get('mobile') if params.get('mobile') else ''

            from_province_id = params.get('from_province_id') if params.get('from_province_id') else ''
            from_city_id = params.get('from_city_id') if params.get('from_city_id') else ''
            from_county_id = params.get('from_county_id') if params.get('from_county_id') else ''
            from_town_id = params.get('from_town_id') if params.get('from_town_id') else ''
            to_province_id = params.get('to_province_id') if params.get('to_province_id') else ''
            to_city_id = params.get('to_city_id') if params.get('to_city_id') else ''
            to_county_id = params.get('to_county_id') if params.get('to_county_id') else ''
            to_town_id = params.get('to_town_id') if params.get('to_town_id') else ''

            goods_type = int(params.get('goods_type')) if params.get('goods_type') else 0
            goods_price_type = int(params.get('goods_price_type')) if params.get('goods_price_type') else 0
            goods_status = int(params.get('goods_status')) if params.get('goods_status') else 0
            is_called = int(params.get('is_called')) if params.get('is_called') else 0
            vehicle_length = str(params.get('vehicle_length')) if params.get('vehicle_length') else 0
            vehicle_type = str(params.get('vehicle_type')) if params.get('vehicle_type') else 0
            region_id = int(params.get('node_id')) if params.get('node_id') else 0
            new_goods_type = int(params.get('new_goods_type')) if params.get('new_goods_type') else 0
            urgent_goods = int(params.get('urgent_goods')) if params.get('urgent_goods') else 0
            is_addition = int(params.get('is_addition')) if params.get('is_addition') else 0
            payment_method = int(params.get('payment_method') or 0)

            # 补全时间
            create_start_time, create_end_time = complement_time(create_start_time, create_end_time)
            register_start_time, register_end_time = complement_time(register_start_time, register_end_time)

            # 校验参数
            if not compare_time(create_start_time, create_end_time):
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='时间参数有误'))

            if not compare_time(register_start_time, register_end_time):
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='时间参数有误'))

            # 当前权限下所有地区
            if not SessionOperationClass.check():
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.UnLogin, msg='请登录'))

            role, locations_id = SessionOperationClass.get_locations()
            if '区镇合伙人' in role or '网点管理员' in role or '城市经理' in role:
                if not region_id:
                    region_id = locations_id
                if str(region_id) not in locations_id:
                    abort(HTTPStatus.Forbidden, **make_result(status=APIStatus.Forbidden, msg='非权限范围内地区'))


            params = {
                "goods_id": goods_id,
                "mobile": mobile,
                'from_province_id': from_province_id,
                'from_city_id': from_city_id,
                'from_county_id': from_county_id,
                'from_town_id': from_town_id,
                'to_province_id': to_province_id,
                'to_city_id': to_city_id,
                'to_county_id': to_county_id,
                'to_town_id': to_town_id,
                "goods_type": goods_type,
                "goods_price_type": goods_price_type,
                "goods_status": goods_status,
                "is_called": is_called,
                "vehicle_length": vehicle_length,
                "vehicle_type": vehicle_type,
                "region_id": region_id,
                "new_goods_type": new_goods_type,
                "urgent_goods": urgent_goods,
                "is_addition": is_addition,
                "create_start_time": create_start_time,
                "create_end_time": create_end_time,
                "register_start_time": register_start_time,
                "register_end_time": register_end_time,
                "payment_method": payment_method
            }
            log.debug("货源列表验证参数{}".format(params))
            return Response(page=page, limit=limit, params=params)

        except Exception as e:
            log.error('Error:{}'.format(e), exc_info=True)
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.Forbidden, msg='请求参数有误'))


class CancelGoodsReason(object):

    @staticmethod
    @make_decorator
    def check_params(params):
        try:
            start_time = int(params.get('start_time', None) or time.time() - 86400 * 7)
            end_time = int(params.get('end_time', None) or time.time() - 86400)
            goods_type = int(params.get('goods_type', None) or 0)
            goods_price_type = int(params.get('goods_price_type', None) or 0)
            region_id = int(params.get('region_id', None) or 0)

            # 当前权限下所有地区
            if not SessionOperationClass.check():
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.UnLogin, msg='请登录'))

            role, locations_id = SessionOperationClass.get_locations()
            if '区镇合伙人' in role or '网点管理员' in role or '城市经理' in role:
                if not region_id:
                    region_id = locations_id
                if str(region_id) not in locations_id:
                    abort(HTTPStatus.Forbidden, **make_result(status=APIStatus.Forbidden, msg='非权限范围内地区'))

            if not compare_time(start_time, end_time):
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='时间参数有误'))

            params = {
                'start_time': start_time,
                'end_time': end_time,
                'goods_type': goods_type,
                'goods_price_type': goods_price_type,
                'region_id': region_id
            }
            return Response(params=params)
        except Exception as e:
            log.error('Error:{}'.format(e), exc_info=True)
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.Forbidden, msg='请求参数有误'))


class GoodsDistributionTrend(object):

    @staticmethod
    @make_decorator
    def check_params(params):
        try:
            start_time = int(params.get('start_time', None) or time.time() - 86400 * 7)
            end_time = int(params.get('end_time', None) or time.time() - 86400)
            periods = int(params.get('periods', None) or 2)
            goods_type = int(params.get('goods_type', None) or 0)
            goods_price_type = int(params.get('goods_price_type', None) or 0)
            region_id = int(params.get('region_id', None) or 0)
            payment_method = int(params.get('payment_method') or 0)

            # 当前权限下所有地区
            if not SessionOperationClass.check():
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.UnLogin, msg='请登录'))

            role, locations_id = SessionOperationClass.get_locations()
            if '区镇合伙人' in role or '网点管理员' in role or '城市经理' in role:
                if not region_id:
                    region_id = locations_id
                if str(region_id) not in locations_id:
                    abort(HTTPStatus.Forbidden, **make_result(status=APIStatus.Forbidden, msg='非权限范围内地区'))

            if not compare_time(start_time, end_time):
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='时间参数有误'))

            params = {
                'start_time': start_time,
                'end_time': end_time,
                'periods': periods,
                'goods_type': goods_type,
                'goods_price_type': goods_price_type,
                'region_id': region_id,
                'payment_method': payment_method
            }

            return Response(params=params)
        except Exception as e:
            log.error('Error:{}'.format(e), exc_info=True)
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.Forbidden, msg='请求参数有误'))
