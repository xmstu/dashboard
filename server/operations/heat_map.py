from server.database import db
from server.meta.decorators import make_decorator, Response
from server.models.heat_map import HeatMapModel


class HeatMap(object):

    @staticmethod
    @make_decorator
    def get_data(params):
        data = HeatMapModel.get_data(db.read_db, params)
        return Response(data=data)
