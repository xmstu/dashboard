from server.database import db
from server.meta.decorators import make_decorator, Response
from server.models.price import PriceTrendModel


class PriceTrend(object):

    @staticmethod
    @make_decorator
    def get_data(params):
        data = PriceTrendModel.get_data(db.read_db, params)
        return Response(params=params, data=data)