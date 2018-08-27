from server.database import db
from server.meta.decorators import make_decorator, Response
from server.models.goods_potential import GoodsPotentialListModel


class GoodsPotentialList(object):

    @staticmethod
    @make_decorator
    def get_potential_goods_list(params):
        data = GoodsPotentialListModel.get_data(db.read_db, params)

        return Response(data=data)