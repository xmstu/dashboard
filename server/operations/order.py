import json

from server.database import db
from server.meta.decorators import make_decorator, Response
from server.models.order import OrdersReceivedStatisticsList, CancelOrderReasonModel, OrderListModel, FreshOwnerModel, \
    FreshDriverModel


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
        fresh_owner_ids = FreshOwnerModel.get_fresh_owner_id(db.read_bi, db.read_db)
        fresh_driver_ids = FreshDriverModel.get_fresh_driver_id(db.read_db)
        data = OrderListModel.get_order_list(db.read_db, page, limit, fresh_owner_ids, fresh_driver_ids, params)

        return Response(data=data, params=params)
