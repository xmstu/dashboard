from server.cache_data import init_regions
from server.database import db
from server.meta.decorators import make_decorator, Response
from server.models.heat_map import HeatMapModel


class HeatMap(object):

    @staticmethod
    @make_decorator
    def get_data(params):

        # 获取城市级别
        region_level = init_regions.get_city_level(params.get('region_id'))

        # 按用户
        if params.get('dimension') == 1:
            data = HeatMapModel.get_user(db.read_bi, params, region_level)
        # 按货源
        elif params.get('dimension') == 2:
            data = HeatMapModel.get_goods(db.read_db, params, region_level)
        # 按车型
        elif params.get('dimension') == 3:
            data = HeatMapModel.get_vehicle(db.read_db, db.read_bi, params, region_level)
        else:
            data = {}

        return Response(params=params, data=data)
