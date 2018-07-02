# -*- coding: utf-8 -*-

import json
from server.utils.date_format import get_date_aggregate

from server.meta.decorators import make_decorator
from server.status import build_result, APIStatus, HTTPStatus, make_result
from server.utils.extend import ExtendHandler


class PromoteEffect(object):

    @staticmethod
    @make_decorator
    def get_add_data(result):
        if result:
            return make_result(APIStatus.Ok), HTTPStatus.Ok
        else:
            return make_result(APIStatus.BadRequest, msg="添加推广人员失败"), HTTPStatus.BadRequest

    @staticmethod
    @make_decorator
    def get_delete_data(result):
        if result:
            return make_result(APIStatus.Ok), HTTPStatus.Ok
        else:
            return make_result(APIStatus.BadRequest, msg="删除推广人员失败"), HTTPStatus.BadRequest

    @staticmethod
    @make_decorator
    def get_result(result, count, params):
        def filter_detail(detail):
            """过滤详情"""
            goods_count = 0
            goods_user_count = 0
            order_over_count_online = 0
            order_over_count_unline = 0
            goods_price = 0
            order_over_price_online = 0
            order_over_price_unline = 0
            # 全部
            if params['goods_type'] == 0:
                goods_count = detail['goods_count_SH'] + detail['goods_count_LH']
                goods_user_count = detail['goods_user_count']
                order_over_count_online = detail['order_over_count_SH_online'] + detail['order_over_count_LH_online']
                order_over_count_unline = detail['order_over_count_SH_unline'] + detail['order_over_count_LH_unline']
                goods_price = detail['goods_price_SH'] + detail['goods_price_LH']
                order_over_price_online = detail['order_over_price_SH_online'] + detail['order_over_price_LH_online']
                order_over_price_unline = detail['order_over_price_SH_unline'] + detail['order_over_price_LH_unline']
            # 同城
            elif params['goods_type'] == 1:
                goods_count = detail['goods_count_SH']
                goods_user_count = detail['goods_user_count_SH']
                order_over_count_online = detail['order_over_count_SH_online']
                order_over_count_unline = detail['order_over_count_SH_unline']
                goods_price = detail['goods_price_SH']
                order_over_price_online = detail['order_over_price_SH_online']
                order_over_price_unline = detail['order_over_price_SH_unline']
            # 跨城
            elif params['goods_type'] == 2:
                goods_count = detail['goods_count_LH']
                goods_user_count = detail['goods_user_count_LH']
                order_over_count_online = detail['order_over_count_LH_online']
                order_over_count_unline = detail['order_over_count_LH_unline']
                goods_price = detail['goods_price_LH']
                order_over_price_online = detail['order_over_price_LH_online']
                order_over_price_unline = detail['order_over_price_LH_unline']

            return {
                'reference_id': detail['user_id'],
                'reference_name': detail['user_name'],
                'reference_mobile': detail['mobile'],
                'user_count': detail['user_count'],
                'wake_up_count': detail['wake_up_count'],
                'goods_count': int(goods_count),
                'goods_user_count': int(goods_user_count),
                'order_over_count_online': int(order_over_count_online),
                'order_over_count_unline': int(order_over_count_unline),
                'goods_price': int(goods_price),
                'order_over_price_online': int(order_over_price_online),
                'order_over_price_unline': int(order_over_price_unline)
            }

        data = []
        for detail in result:
            data.append(filter_detail(detail))
        return build_result(APIStatus.Ok, count=count, data=data), HTTPStatus.Ok


class PromoteQuality(object):

    @staticmethod
    @make_decorator
    def get_result(params, data, before_promote_count):
        # 日期聚合
        xAxis, series = get_date_aggregate(params['start_time'], params['end_time'], params['periods'], data, date_field='create_time', number_field='count')

        # 累计
        if params['dimension'] == 1 and params['data_type'] == 2:
            series = [sum(series[: i + 1]) + before_promote_count if i > 0 else series[i] + before_promote_count for i
                      in range(len(series))]

        series = json.loads(json.dumps(series, default=ExtendHandler.handler_to_float))
        # 按月分段，返回总和
        if params['periods'] == 4:
            data = {'xAxis': xAxis, 'series': series, 'last_month': sum(series)}
        else:
            data = {'xAxis': xAxis, 'series': series}
        return make_result(APIStatus.Ok, data=data), HTTPStatus.Ok
