from server.database import db
from server.meta.decorators import make_decorator, Response
from server.models.transport import TransportTrendModel


class TransportTrend(object):

    @staticmethod
    @make_decorator
    def get_trend(params):
        data = TransportTrendModel.get_data(db.read, params)

        return Response(data=data)
