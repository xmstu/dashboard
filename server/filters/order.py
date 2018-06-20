import json

from server.meta.decorators import make_decorator
from server.status import make_result, APIStatus, HTTPStatus
from server.utils.extend import ExtendHandler, get_struct_data, get_xAxis


class OrdersReceivedStatistics(object):

    @staticmethod
    @make_decorator
    def get_result(data, params):
        order_count_series = get_struct_data(data['data'], params, 'order_counts')
        order_sum_price_series = get_struct_data(data['data'], params, 'order_sum_price')
        xAxis = get_xAxis(params)

        order_sum_price_series = json.loads(json.dumps(order_sum_price_series, default=ExtendHandler.handler_to_float))

        if params.get('dimension') == 1:
            series = order_count_series
        elif params.get('dimension') == 2:
            series = order_sum_price_series
        else:
            series = [0 for _ in xAxis]

        ret = {
            'xAxis': xAxis,
            'series': series
        }
        return make_result(APIStatus.Ok, data=ret), HTTPStatus.Ok


class CancelOrderReason(object):

    @staticmethod
    @make_decorator
    def get_result(data):
        # TODO 过滤参数

        return make_result(APIStatus.Ok, data=data), HTTPStatus.Ok


class OrderList(object):

    @staticmethod
    @make_decorator
    def get_result(data):
        # TODO 过滤参数

        return make_result(APIStatus.Ok), HTTPStatus.Ok
