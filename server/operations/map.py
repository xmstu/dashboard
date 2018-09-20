from server.cache_data import init_regions
from server.database import db
from server.meta.decorators import make_decorator, Response
from server.models.goods import FreshConsignor
from server.models.map import DistributionMapModel, GoodsMapModel, UsersMapModel
from server.status import APIStatus, HTTPStatus, make_resp


class DistributionMap(object):

    @staticmethod
    @make_decorator
    def get_data(params):

        # 获取城市级别
        region_level = init_regions.get_map_city_level(params.get('region_id'))

        # 按用户
        if params.get('dimension') == 1:
            data = DistributionMapModel.get_user(db.read_bi, params, region_level)
        # 按货源
        elif params.get('dimension') == 2:
            data = DistributionMapModel.get_goods(db.read_db, params, region_level)
        # 按运力
        elif params.get('dimension') == 3:
            data = DistributionMapModel.get_vehicle(db.read_db, db.read_bi, params, region_level)
        # 按订单
        elif params.get('dimension') == 4:
            data = DistributionMapModel.get_order(db.read_db, params, region_level)
        else:
            data = {}

        return Response(params=params, data=data)


class GoodsMap(object):

    @staticmethod
    @make_decorator
    def get_data(params):
        if params.get('special_tag') == 1:
            user_id_list = FreshConsignor.get_user_id_list(db.read_db, params.get('role_region_id'))
        else:
            user_id_list = None
        max_count, data = GoodsMapModel.get_data(db.read_db, user_id_list, params)
        return make_resp(status=APIStatus.Ok, max_count=max_count, data=data), HTTPStatus.Ok


class UsersMap(object):

    @staticmethod
    @make_decorator
    def get_data(params):
        data = UsersMapModel.get_data(db.read, params)
        return Response(data=data)
