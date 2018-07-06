from server.database import db
from server.meta.decorators import make_decorator, Response
from server.models.heat_map import HeatMapModel


class HeatMap(object):

    @staticmethod
    @make_decorator
    def get_data(params):
        # 按用户
        if params.get('dimension') == 1:
            data = HeatMapModel.get_user(db.read_bi, params)
        # 按货源
        elif params.get('dimension') == 2:
            data = HeatMapModel.get_goods(db.read_db, params)
        # 按车型
        elif params.get('dimension') == 3:
            data = HeatMapModel.get_vehicle(db.read_db, params)
        else:
            data = {}

        return Response(data=data)
