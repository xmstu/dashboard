#!/usr/bin/python
# -*- coding:utf-8 -*-
# author=hexm

from flask_restplus import Resource

import server.document.order as doc
from server import api
from server.filters import order_list_get_result, orders_received_statistics_get_result
from server.meta.redis_cache import redis_cache
from server.operations import order_list_get_data, cancel_order_get_data, orders_received_statistics_get_data
from server.status import make_resp, APIStatus, HTTPStatus
from server.utils.request import get_all_arg
from server.verify import order_list_check_params, cancel_order_check_params, orders_received_statistics_check_params


class OrdersReceivedStatistics(Resource):

    @staticmethod
    @doc.request_order_received_statistics_param
    @redis_cache(expire_time=7200)
    def get():
        """订单趋势统计"""
        params = orders_received_statistics_check_params(params=get_all_arg())
        data = orders_received_statistics_get_data(params)
        result = orders_received_statistics_get_result(data, params)
        return result


class CancelOrderReason(Resource):

    @staticmethod
    @doc.request_cancel_order_reason_param
    @redis_cache(expire_time=7200)
    def get():
        """取消订单原因统计"""
        params = cancel_order_check_params(params=get_all_arg())
        data = cancel_order_get_data(params)
        return make_resp(APIStatus.Ok, data=data), HTTPStatus.Ok


class OrderList(Resource):

    @staticmethod
    @doc.request_order_list_param
    @redis_cache(expire_time=3600)
    def get():
        """订单列表"""
        params = order_list_check_params(params=get_all_arg())
        data = order_list_get_data(params)
        result = order_list_get_result(data)

        return result


ns = api.namespace('order', description='订单接口')
ns.add_resource(OrdersReceivedStatistics, '/statistics/')
ns.add_resource(CancelOrderReason, '/cancel_reason/')
ns.add_resource(OrderList, '/list/')
