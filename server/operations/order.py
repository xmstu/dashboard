from server.database import db
from server.meta.decorators import make_decorator, Response
from server.models.order import OrdersReceivedStatisticsList, CancelOrderReasonModel


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
    def get_data(params):
        data = model.get_data(db.read, params)
        if not data:
            abort(HTTPStatus.NotFound, **make_result(status=APIStatus.NotFound, msg='找不到数据'))
        return Response(data=data)