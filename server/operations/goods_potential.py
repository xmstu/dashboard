from server.database import db
from server.models.goods_potential import GoodsPotentialListModel, GoodsPotentialDistributionTrendModel


def get_goods_potential_distribution_trend(params):
    if params.get('business') == 1:
        data = GoodsPotentialDistributionTrendModel.get_ftl_data(db.read_db, params)
    elif params.get('business') == 2:
        data = GoodsPotentialDistributionTrendModel.get_ltl_data(db.read_db, params)
    else:
        data = []
    return data


def get_potential_goods_list(params):
    if params.get('business') == 1:
        data = GoodsPotentialListModel.get_ftl_data(db.read_db, params)
    elif params.get('business') == 2:
        data = GoodsPotentialListModel.get_ltl_data(db.read_db, params)
    else:
        data = []
    return data
