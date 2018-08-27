from server.database import db
from server.meta.decorators import make_decorator, Response
from server.models.goods_potential import GoodsPotentialListModel, GoodsPotentialDistributionTrendModel


class GoodsPotentialDistributionTrend(object):

    @staticmethod
    @make_decorator
    def get_goods_potential_distribution_trend(params):
        data = GoodsPotentialDistributionTrendModel.get_data(db.read, params)
        return Response(data=data)


class GoodsPotentialList(object):

    @staticmethod
    @make_decorator
    def get_potential_goods_list(page, limit, params):
        data = GoodsPotentialListModel.get_data(db.read_db, page, limit, params)

        return Response(data=data)