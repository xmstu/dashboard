import json

from server.database import db
from server.meta.decorators import make_decorator, Response
from server.models.order import OrdersReceivedStatisticsList, CancelOrderReasonModel, OrderListmodel
from server.utils.extend import ExtendHandler


class OrdersReceivedStatistics(object):

    @staticmethod
    @make_decorator
    def get_data(params):

        data = OrdersReceivedStatisticsList.get_order_received_statistics_list(db.read_db, params)

        return Response(data=data, params=params)


class CancelOrderReason(object):

    @staticmethod
    @make_decorator
    def get_data(params):
        data = CancelOrderReasonModel.get_cancel_order_reason(db.read_db, params)

        return Response(data=data)


class OrderList(object):

    @staticmethod
    @make_decorator
    def get_data(page, limit, params):
        data = OrderListmodel.get_order_list(db.read_db, page, limit, params)

        return Response(data=data, params=params)