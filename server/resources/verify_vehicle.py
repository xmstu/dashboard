from flask_restplus import Resource

from server import api, log
from server.meta.decorators import Response
from server.utils.request import get_all_arg, get_arg_int
from server import verify, operations, filters
import server.document.verify_vehicle as doc
import server.verify.general as general_verify


class VerifyVehicleList(Resource):

    @staticmethod
    @doc.verify_vehicle_list_param
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


ns = api.namespace('vehicle', description='认证车辆统计')
ns.add_resource(VerifyVehicleList, '/list/')
