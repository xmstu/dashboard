from flask_restplus import Resource

from server import api, log
from server.meta.decorators import Response
from server.utils.request import get_all_arg, get_arg_int
from server import verify, operations, filters
import server.document.transport as doc
import server.verify.general as general_verify


class TransportRadar(Resource):

    @staticmethod
    @doc.transport_radar_param
    @filters.TransportRadar.get_result(data=dict)
    @operations.TransportRadar.get_trend(params=dict)
    @verify.TransportRadar.check_params(params=dict)
    def get():
        """运力雷达"""
        resp = Response(params=get_all_arg())

        return resp


class TransportList(Resource):

    @staticmethod
    @doc.transport_list_param
    @filters.TransportList.get_result(data=dict)
    @operations.TransportList.get_list(page=int, limit=int, params=dict)
    @verify.TransportList.check_params(page=int, limit=int, params=dict)
    @general_verify.Paging.check_paging(page=int, limit=int, params=dict)
    def get():
        """运力列表"""
        resp = Response(
            page=get_arg_int('page', 1),
            limit=get_arg_int('limit', 10),
            params=get_all_arg())

        log.debug('获取订单列表参数{}'.format(resp))
        return resp


ns = api.namespace('transport', description='运力统计')
ns.add_resource(TransportRadar, '/radar/')
ns.add_resource(TransportList, '/list/')
