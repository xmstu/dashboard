from flask_restplus import Resource

from server import verify, operations, filters, api
from server.meta.decorators import Response
from server.utils.request import get_all_arg
import server.document.heat_map as doc


class HeatMap(Resource):

    @staticmethod
    @doc.heat_map_param
    @filters.HeatMap.get_result(params=dict, data=dict)
    @operations.HeatMap.get_data(params=dict)
    @verify.HeatMap.check_params(params=dict)
    def get():
        resp = Response(params=get_all_arg())

        return resp


ns = api.namespace('map', description='热点图')
ns.add_resource(HeatMap, '/heat_map/')