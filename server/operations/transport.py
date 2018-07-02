from server.database import db
from server.meta.decorators import make_decorator, Response
from server.models.transport import TransportRadarModel


class TransportRadar(object):

    @staticmethod
    @make_decorator
    def get_trend(params):
        data = TransportRadarModel.get_data(db.read_db, params)

        return Response(data=data)
