from flask_restplus import Resource

from server import verify, operations, filters, api
from server.meta.decorators import Response
from server.utils.request import get_all_arg
import server.document.price as doc


class PriceTrend(Resource):

    @staticmethod
    @doc.price_trend_param
    @filters.PriceTrend.get_result(data=dict)
    @operations.PriceTrend.get_data(params=dict)
    @verify.PriceTrend.check_params(params=dict)
    def get():
        resp = Response(params=get_all_arg())

        return resp


ns = api.namespace('price', description='价格统计')
ns.add_resource(PriceTrend, '/price_trend/')