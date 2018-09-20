# -*- coding: utf-8 -*-

from flask_restful import abort
import time

from server import log
from server.meta.decorators import make_decorator, Response
from server.status import HTTPStatus, make_resp, APIStatus
from server.meta.session_operation import SessionOperationClass
from server.utils.extend import complement_time, compare_time
from server.utils.role_regions import get_role_regions


class CityResourceBalance(object):
    @staticmethod
    @make_decorator
    def check_params(params):
        try:
            if not SessionOperationClass.check():
                abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.UnLogin, msg='请登录'))

            params['start_time'] = int(params.get('start_time') or time.time() - 86400*7)
            params['end_time'] = int(params.get('end_time') or time.time())
            params['region_id'] = int(params.get('region_id') or 0)
            params['goods_price_type'] = int(params.get('goods_price_type') or 1)
            params['haul_dist'] = int(params.get('haul_dist') or 0)

            # 当前权限下所有地区
            params['region_id'] = get_role_regions(params['region_id'])
            # 补全时间
            params['start_time'], params['end_time'] = complement_time(params['start_time'], params['end_time'])
            # 校验时间
            if not compare_time(params['start_time'], params['end_time']):
                abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='时间参数有误'))
            log.debug(
                '获取供需平衡数据统计检查参数: [region_id: %s][haul_dist: %s][goods_price_type: %s][start_time: %s][end_time: %s]'
                % (params['region_id'], params['haul_dist'], params['goods_price_type'], params['start_time'],
                   params['end_time']))
            return Response(params=params)
        except Exception as e:
            log.error('请求供需平衡表有误:{}'.format(e))
            abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='请求供需平衡表参数有误'))


class CityOrderList(object):

    @staticmethod
    @make_decorator
    def check_params(page, limit, params):
        try:
            if not SessionOperationClass.check():
                abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.UnLogin, msg='请登录'))

            params['goods_type'] = int(params.get('goods_type', None) or 0)
            params['goods_price_type'] = int(params.get('goods_price_type', None) or 0)
            params['vehicle_length'] = str(params.get('vehicle_length', None) or '')
            params['is_called'] = int(params.get('is_called', None) or 0)
            params['is_addition'] = int(params.get('is_addition', None) or 0)
            params['region_id'] = int(params.get('region_id', None) or 0)
            params['spec_tag'] = int(params.get('spec_tag', None) or 0)
            params['mobile'] = int(params.get('mobile', None) or 0)

            # 当前权限下所有地区
            params['region_id'] = get_role_regions(params['region_id'])
            return Response(page=page, limit=limit, params=params)

        except Exception as e:
            log.error('最新接单货源参数错误:{}'.format(e), exc_info=True)
            abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.Forbidden, msg='请求参数有误'))

