
from server.database import db
from server.meta.decorators import make_decorator, Response
from server.models.city import CityOrderListModel


class CityOrderListDecorator(object):

    @staticmethod
    @make_decorator
    def get_data(page, limit, params):
        data = CityOrderListModel.get_data(db.read_db, page, limit, params)
        return Response(data=data)