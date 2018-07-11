from server.database import db
from server.meta.decorators import make_decorator, Response
from server.models.transport import TransportRadarModel, TransportListModel


class TransportRadar(object):

    @staticmethod
    @make_decorator
    def get_trend(params):
        data = TransportRadarModel.get_data(db.read_db, db.read_bi, params)

        return Response(data=data)


class TransportList(object):

    @staticmethod
    @make_decorator
    def get_list(page, limit, params):
        data = TransportListModel.get_data(db.read_db, db.read_bi, page, limit, params)

        return Response(data=data)
