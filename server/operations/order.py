from server.database import db
from server.meta.decorators import make_decorator, Response
from server.models.order import OrdersReceivedStatisticsList


class OrdersReceivedStatistics(object):

    @staticmethod
    @make_decorator
    def get_data(params):

        data = OrdersReceivedStatisticsList.get_order_received_statistics_list(db.read_db, params)

        return Response(data=data)