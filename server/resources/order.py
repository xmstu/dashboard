#!/usr/bin/python
# -*- coding:utf-8 -*-
# author=hexm
from flask_restplus import Resource

from server import log, verify, operations, filters, api
import server.document.order as doc
from server.meta.decorators import Response
from server.utils.request import get_all_arg


class OrdersReceivedStatistics(Resource):

    @staticmethod
    @doc.request_order_received_statistics_param
    @filters.OrdersReceivedStatistics.get_result(data=dict, params=dict)
    @operations.OrdersReceivedStatistics.get_data(params=dict)
    @verify.OrdersReceivedStatistics.check_params(params=dict)
    def get():

        resp = Response(params=get_all_arg())

        return resp


class CancelOrderReason(Resource):

    @staticmethod
    @doc.request_cancel_order_reason_param
    @filters.CancelOrderReason.get_result(data=dict, params=dict)
    @operations.CancelOrderReason.get_data(params=dict)
    @verify.CancelOrderReason.check_params(params=dict)
    def get():

        resp = Response(params=get_all_arg())

        return resp


class OrderList(Resource):

    @staticmethod
    @doc.request_order_list_param
    @filters.OrderList.get_result(data=dict, params=dict)
    @operations.OrderList.get_data(params=dict)
    @verify.OrderList.check_params(params=dict)
    def get():
        pass


ns = api.namespace('order', description='订单接口')
ns.add_resource(OrdersReceivedStatistics, '/statistics/')
ns.add_resource(CancelOrderReason, '/cancel_reason/')
ns.add_resource(OrderList, '/list/')
