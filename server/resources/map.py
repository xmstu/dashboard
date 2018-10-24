from flask_restplus import Resource

import server.document.map as doc
from server import verify, operations, filters, api
from server.filters import distribution_map_get_result
from server.meta.decorators import Response
from server.meta.redis_cache import redis_cache
from server.operations import distribution_map_get_data, goods_map_get_data, goods_map_post_data
from server.utils.request import get_all_arg, get_payload
from server.utils.role_regions import get_role_regions
from server.verify import distribution_map_check_params, goods_map_check_params, check_map_post_params


class DistributionMap(Resource):

    @staticmethod
    @doc.distribution_map_param
    @redis_cache(expire_time=86400)
    def get():
        params = distribution_map_check_params(params=get_all_arg())
        data = distribution_map_get_data(params)
        return distribution_map_get_result(params, data)


class GoodsMap(Resource):

    @staticmethod
    @doc.goods_map_param
    @redis_cache(expire_time=3600)
    def get():
        params = get_all_arg()
        params["role_region_id"] = get_role_regions(0)
        params = goods_map_check_params(params)
        return goods_map_get_data(params)

    @staticmethod
    @doc.goods_map_param_post
    def post():
        params = check_map_post_params(params=get_payload())
        params = goods_map_check_params(params)
        return goods_map_post_data(params)


class UsersMap(Resource):

    @staticmethod
    @doc.users_map_param
    @filters.UsersMap.get_result(params=dict, data=dict)
    @operations.UsersMap.get_data(params=dict)
    @verify.UsersMap.check_params(params=dict)
    def get():
        resp = Response(params=get_all_arg())

        return resp


ns = api.namespace('map', description='地图工具')
ns.add_resource(DistributionMap, '/distribution_map/')
ns.add_resource(GoodsMap, '/goods_map/')
ns.add_resource(UsersMap, '/users_map/')
