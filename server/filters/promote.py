# -*- coding: utf-8 -*-

import json
from server.utils.date_format import get_date_aggregate

from server.meta.decorators import make_decorator
from server.status import make_resp, APIStatus, HTTPStatus, make_resp
from server.utils.extend import ExtendHandler


class PromoteEffect(object):

    @staticmethod
    @make_decorator
    def get_add_data(result):
        if result:
            return make_resp(APIStatus.Ok), HTTPStatus.Ok
        else:
            return make_resp(APIStatus.BadRequest, msg="添加推广人员失败"), HTTPStatus.BadRequest

    @staticmethod
    @make_decorator
    def get_delete_data(result):
        if result:
            return make_resp(APIStatus.Ok), HTTPStatus.Ok
        else:
            return make_resp(APIStatus.BadRequest, msg="删除推广人员失败"), HTTPStatus.BadRequest


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

        series = json.loads(json.dumps(series, default=ExtendHandler.handler_to_int))
        # 按月分段，返回总和
        if params['periods'] == 4:
            data = {'xAxis': xAxis, 'series': series, 'last_month': sum(series)}
        else:
            data = {'xAxis': xAxis, 'series': series}
        return make_resp(APIStatus.Ok, data=data), HTTPStatus.Ok
