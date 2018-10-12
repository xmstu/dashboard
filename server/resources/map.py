from flask_restplus import Resource

import server.document.map as doc
from server import verify, operations, filters, api
from server.meta.decorators import Response
from server.utils.request import get_all_arg, get_payload
from server.utils.role_regions import get_role_regions


class DistributionMap(Resource):

    @staticmethod
    @doc.distribution_map_param
    @filters.DistributionMap.get_result(params=dict, data=dict)
    @operations.DistributionMap.get_data(params=dict)
    @verify.DistributionMap.check_params(params=dict)
    def get():
        resp = Response(params=get_all_arg())

        return resp


class GoodsMap(Resource):

    @staticmethod
    @doc.goods_map_param
    @operations.GoodsMap.get_data(params=dict)
    @verify.GoodsMap.check_params(params=dict)
    def get():
        params = get_all_arg()
        params["role_region_id"] = get_role_regions(0)

        return Response(params=params)

    @staticmethod
    @doc.goods_map_param_post
    @operations.GoodsMap.post_data(params=dict)
    @verify.GoodsMap.check_params(params=dict)
    @verify.GoodsMap.check_post_params(params=dict)
    def post():
        return Response(params=get_payload())


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
