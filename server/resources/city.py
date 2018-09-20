# -*- coding: utf-8 -*-

from flask_restplus import Resource

from server import api, log
import server.verify.general as general_verify
from server.meta.decorators import Response
import server.document.city as doc
from server import verify, operations, filters
from server.utils.request import get_arg_int, get_all_arg


class CityResourceBalance(Resource):
    @staticmethod
    @doc.request_city_resource_balance
    @filters.CityResourceBalance.get_result(goods=list, vehicle=list, params=dict)
    @operations.CityResourceBalance.get_data(params=dict)
    @verify.CityResourceBalance.check_params(params=dict)
    def get():
        """供需平衡数据统计"""
        resp = Response(params=get_all_arg())
        log.info('获取供需平衡数据统计请求: [region_id: %s][goods_type: %s][start_time: %s][end_time: %s]'
                 % (resp['params'].get('region_id', 0), resp['params'].get('goods_type', 0), resp['params'].get('start_time', 0), resp['params'].get('end_time', 0)))
        return resp


class CityLatestOpenOrderList(Resource):
    @staticmethod
    @doc.request_order_list_param
    @filters.CityOrderListFilterDecorator.get_result(data=dict)
    @operations.CityOrderListDecorator.get_data(page=int, limit=int, params=dict)
    @verify.CityOrderList.check_params(page=int, limit=int, params=dict)
    @general_verify.Paging.check_paging(page=int, limit=int, params=dict)
    def get():
        """最新接单货源"""
        resp = Response(page=get_arg_int('page', 1),
                        limit=get_arg_int('limit', 10),
                        params=get_all_arg())
        log.info('最新接单货源请求参数:{}'.format(resp))
        return resp


class CityNearbyCars(Resource):
    @staticmethod
    @doc.request_nearby_cars_param
    @filters.CityNearbyCars.get_result(data=dict, goods_type=int)
    @operations.CityNearbyCars.get_data(goods_id=int, goods_type=int)
    def get(id):
        """货源附近的车"""
        resp = Response(goods_id=id, goods_type=get_arg_int('goods_type', 1))
        log.info('货源附近的车:[goods_id: {}]'.format(id))
        return resp


ns = api.namespace('city', description='城市概况')
ns.add_resource(CityResourceBalance, '/resource/')
ns.add_resource(CityLatestOpenOrderList, '/latest_orders/')
ns.add_resource(CityNearbyCars, '/nearby_cars/<int:id>')

