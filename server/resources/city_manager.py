# -*- coding: utf-8 -*-

from flask_restplus import Resource

from server import api, log
from server.meta.decorators import Response
from server.utils.request import get_all_arg
from server import verify, operations, filters
import server.document.city_manager as doc

class cityManager(Resource):
    @staticmethod
    @doc.request_city_manager
    @filters.cityManagerFilter.filter_data(data=list)
    @operations.cityManagerOperation.get_city_manager_data(params=dict)
    @verify.CityManagerVerify.check_params(params=dict)
    def get():
        """城市经理提成接口"""
        resp = Response(params=get_all_arg())
        log.info('获取城市经理提成请求: [mobile: %s][start_time: %s][end_time: %s]'
                 % (resp['params'].get('mobile', 0), resp['params'].get('start_time', 0), resp['params'].get('end_time', 0)))
        return resp

ns = api.namespace('city_manager', description='城市经理')
ns.add_resource(cityManager, '/promoter')