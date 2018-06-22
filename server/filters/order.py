import json

from server.meta.decorators import make_decorator
from server.status import make_result, APIStatus, HTTPStatus, build_result
from server.utils.extend import ExtendHandler, get_struct_data, get_xAxis


class OrdersReceivedStatistics(object):

    @staticmethod
    @make_decorator
    def get_result(data, params):
        complete_order_count_series = get_struct_data(data['complete_order'], params, 'order_counts')
        complete_order_sum_price_series = get_struct_data(data['complete_order'], params, 'order_sum_price')

        pending_order_count_series = get_struct_data(data['pending_order'], params, 'order_counts')
        pending_order_sum_price_series = get_struct_data(data['pending_order'], params, 'order_sum_price')

        cancel_order_count_series = get_struct_data(data['cancel_order'], params, 'order_counts')
        cancel_order_sum_price_series = get_struct_data(data['cancel_order'], params, 'order_sum_price')

        xAxis = get_xAxis(params)

        complete_order_count_series = json.loads(json.dumps(complete_order_count_series, default=ExtendHandler.handler_to_float))
        pending_order_count_series = json.loads(json.dumps(pending_order_count_series, default=ExtendHandler.handler_to_float))
        cancel_order_count_series = json.loads(json.dumps(cancel_order_count_series, default=ExtendHandler.handler_to_float))

        complete_order_sum_price_series = json.loads(json.dumps(complete_order_sum_price_series, default=ExtendHandler.handler_to_float))
        pending_order_sum_price_series = json.loads(json.dumps(pending_order_sum_price_series, default=ExtendHandler.handler_to_float))
        cancel_order_sum_price_series = json.loads(json.dumps(cancel_order_sum_price_series, default=ExtendHandler.handler_to_float))

        if params.get('dimension') == 1:
            complete_series = complete_order_count_series
            pending_series = pending_order_count_series
            cancel_series = cancel_order_count_series
        elif params.get('dimension') == 2:
            complete_series = complete_order_sum_price_series
            pending_series = pending_order_sum_price_series
            cancel_series = cancel_order_sum_price_series
        else:
            complete_series = [0 for _ in xAxis]
            pending_series = [0 for _ in xAxis]
            cancel_series = [0 for _ in xAxis]

        ret = {
            'xAxis': xAxis,
            'complete_series': complete_series,
            'pending_series': pending_series,
            'cancel_series': cancel_series
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
    def get_result(data, params):
        # TODO 过滤参数
        data = json.loads(json.dumps(data, default=ExtendHandler.handler_to_float))
        return build_result(APIStatus.Ok, count=data['count'], data=data['order_list']), HTTPStatus.Ok
