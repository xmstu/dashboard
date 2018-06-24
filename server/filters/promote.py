# -*- coding: utf-8 -*-

import json
from server.utils.date_format import get_date_aggregate

from server.meta.decorators import make_decorator
from server.status import build_result, APIStatus, HTTPStatus, make_result
from server.utils.extend import ExtendHandler


class PromoteEffect(object):

    @staticmethod
    @make_decorator
    def get_add_data(data):
        if data:
            return make_result(APIStatus.Ok), HTTPStatus.Ok
        else:
            return make_result(APIStatus.BadRequest, msg="用户不存在或不能重复添加推荐人"), HTTPStatus.BadRequest

    @staticmethod
    @make_decorator
    def get_delete_data(data):
        if data:
            return make_result(APIStatus.Ok), HTTPStatus.Ok
        else:
            return make_result(APIStatus.BadRequest), HTTPStatus.BadRequest

    @staticmethod
    @make_decorator
    def get_result(extension_worker_list, promote_effect_list, params):

        # 拼接结果
        ex = extension_worker_list['promote_effect_detail']
        for i in ex:
            i['reference_name'] = i.get('reference_name', '')
            i['reference_mobile'] = i.get('reference_mobile', '')
            i['user_count'] = i.get('user_count', None) or 0
            i['wake_up_count'] = i.get('wake_up_count', None) or 0
            i['goods_count'] = i.get('goods_count', None) or 0
            i['goods_user_count'] = i.get('goods_user_count', None) or 0
            i['goods_price'] = i.get('goods_price', None) or 0
            i['order_over_price'] = i.get('order_over_price', None) or 0
            i['order_over_count'] = i.get('order_over_count', None) or 0
        ex_count = extension_worker_list['count']

        pr = promote_effect_list['promote_effect_detail']
        for i in pr:
            i['reference_name'] = i.get('reference_name', '')
            i['reference_mobile'] = i.get('reference_mobile', '')
            i['user_count'] = i.get('user_count', None) or 0
            i['wake_up_count'] = i.get('wake_up_count', None) or 0
            i['goods_count'] = i.get('goods_count', None) or 0
            i['goods_user_count'] = i.get('goods_user_count', None) or 0
            i['goods_price'] = i.get('goods_price', None) or 0
            i['order_over_price'] = i.get('order_over_price', None) or 0
            i['order_over_count'] = i.get('order_over_count', None) or 0
        pr_count = promote_effect_list['count']

        if params['role_type'] or params['goods_type'] or params['is_actived'] or params['is_car_sticker'] or (params['start_time'] and params['end_time']):
            detail_dict_list = pr
            count = pr_count
        else:
            detail_dict_list = ex
            count = ex_count

        promote_effect_detail = json.loads(json.dumps(detail_dict_list, default=ExtendHandler.handler_to_float))
        return build_result(APIStatus.Ok, count=count, data=promote_effect_detail), HTTPStatus.Ok


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
        # 新增
        else:
            pass
        series = json.loads(json.dumps(series, default=ExtendHandler.handler_to_float))
        return make_result(APIStatus.Ok, data={'xAxis': xAxis, 'counts_series': series}), HTTPStatus.Ok
