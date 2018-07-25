# -*- coding: utf-8 -*-

from flask_restful import abort
import time

from server import log
from server.meta.decorators import make_decorator, Response
from server.status import HTTPStatus, make_result, APIStatus
from server.meta.session_operation import sessionOperationClass

class CityResourceBalance(object):
    @staticmethod
    @make_decorator
    def check_params(params):
        start_time = int(params.get('start_time')) if params.get('start_time') else time.time() - 8 * 60 * 60 * 24
        end_time = int(params.get('end_time')) if params.get('end_time') else time.time() - 60 * 60 * 24
        region_id = int(params.get('region_id')) if params.get('region_id') else 0
        goods_price_type = int(params.get('goods_price_type')) if params.get('goods_price_type') else 1
        haul_dist = int(params.get('haul_dist')) if params.get('haul_dist') else 0

        if start_time and end_time:
            if start_time <= end_time:
                pass
            else:
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='时间参数有误'))
        elif not start_time and not end_time:
            pass
        else:
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='时间参数有误'))

        # 当前权限下所有地区
        role, locations_id = sessionOperationClass.get_locations()
        if role in (2, 3, 4) and not region_id:
            region_id = locations_id

        params = {
            'start_time': start_time,
            'end_time': end_time,
            'region_id': region_id,
            'haul_dist': haul_dist,
            'goods_price_type': goods_price_type
        }
        log.debug('获取供需平衡数据统计检查参数: [region_id: %s][haul_dist: %s][goods_price_type: %s][start_time: %s][end_time: %s]'
                 % (params['region_id'], params['haul_dist'], params['goods_price_type'], params['start_time'], params['end_time']))
        return Response(params=params)


class CityOrderList(object):

    @staticmethod
    @make_decorator
    def check_params(page, limit, params):
        # 通过params获取参数
        try:
            goods_type = int(params.get('goods_type', None) or 0)
            goods_price_type = int(params.get('goods_price_type', None) or 0)
            vehicle_length = str(params.get('vehicle_length', None) or '')
            is_called = int(params.get('is_called', None) or 0)
            is_addition = int(params.get('is_addition', None) or 0)
            region_id = int(params.get('node_id', None) or 0)
            spec_tag = int(params.get('spec_tag', None) or 0)
            mobile = int(params.get('mobile', None) or 0)

            # 当前权限下所有地区
            role, locations_id = sessionOperationClass.get_locations()
            if role in (2, 3, 4) and not region_id:
                region_id = locations_id

            params = {
                "goods_type": goods_type,
                "goods_price_type": goods_price_type,
                "is_called": is_called,
                "vehicle_length": vehicle_length,
                "region_id": region_id,
                "spec_tag": spec_tag,
                "is_addition": is_addition,
                "mobile": mobile
            }
            return Response(page=page, limit=limit, params=params)

        except Exception as e:
            log.error('最新接单货源参数错误:{}'.format(e), exc_info=True)
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='请求参数有误'))

