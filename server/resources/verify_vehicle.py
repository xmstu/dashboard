from flask_restplus import Resource

import server.document.verify_vehicle as doc
from server import api, log
from server.filters import verify_vehicle_get_result
from server.meta.redis_cache import redis_cache
from server.operations import verify_vehicle_get_list
from server.utils.request import get_all_arg
from server.verify import verify_vehicle_check_params


class VerifyVehicleList(Resource):

    @staticmethod
    @doc.verify_vehicle_list_param
    @redis_cache(expire_time=1800)
    def get():
        """认证车辆列表"""
        params = verify_vehicle_check_params(params=get_all_arg())
        log.debug('获取认证车辆列表参数:{}'.format(params))
        data = verify_vehicle_get_list(params)
        return verify_vehicle_get_result(data)


ns = api.namespace('vehicle', description='认证车辆统计')
ns.add_resource(VerifyVehicleList, '/list/')
