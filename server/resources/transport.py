from flask_restplus import Resource

from server import api
from server.meta.decorators import Response
from server.utils.request import get_all_arg
from server import verify, operations, filters
import server.document.transport as doc


class TransportTrend(Resource):

    @staticmethod
    @doc.transport_trend_param
    @filters.TransportTrend.get_result()
    @operations.TransportTrend.get_trend(params=dict)
    @verify.TransportTrend.check_params(params=dict)
    def get():
        resp = Response(params=get_all_arg())

        return resp


class TransportRadar(Resource):

    @staticmethod
    # @doc.transport_radar_param
    def get():
        pass


class TransportList(Resource):

    @staticmethod
    # @doc.transport_list_param
    def get():
        pass


ns = api.namespace('transport', description='运力统计')
ns.add_resource(TransportTrend, '/trend/')
ns.add_resource(TransportRadar, '/radar/')
ns.add_resource(TransportList, '/list/')
