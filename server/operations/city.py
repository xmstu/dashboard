# -*- coding: utf-8 -*-
from server import log
from server.database import db, pyredis
from server.meta.decorators import make_decorator, Response
from server.models.city import CityOrderListModel, CityResourceBalanceModel, CityNearbyCarsModel
from server.status import HTTPStatus, make_result, APIStatus

from flask_restful import abort


class CityResourceBalance(object):
    @staticmethod
    @make_decorator
    def get_data(params):
        # 货源数据
        goods = CityResourceBalanceModel.get_goods_data(db.read_db, params)
        # 接单车型
        vehicle = CityResourceBalanceModel.get_booking_data(db.read_db, params)
        log.info('获取供需平衡数据统计成功: [region_id: %s][goods_type: %s][start_time: %s][end_time: %s]'
                 % (params['region_id'], params['goods_type'], params['start_time'], params['end_time']))
        return Response(goods=goods, vehicle=vehicle, params=params)


class CityOrderListDecorator(object):

    @staticmethod
    @make_decorator
    def get_data(page, limit, params):
        data = CityOrderListModel.get_data(db.read_db, page, limit, params)
        log.info('获取最新接单货源成功: [params: %s]' % params)
        return Response(data=data)


class CityNearbyCars(object):

    @staticmethod
    @make_decorator
    def get_data(goods_id, goods_type):
        # 获取货源信息
        goods = CityNearbyCarsModel.get_goods(db.read_db, goods_id)
        if not goods:
            return Response(data={}, goods_type=goods_type)
        # 附近车辆
        nearby_vehicle = pyredis['nearby_vehicle']
        dispatcher_nearby = nearby_vehicle.read_georadius('dispatch.vehicle.nearby', goods['from_longitude'], goods['from_latitude'], 5, 'km')
        if not dispatcher_nearby:
            return Response(data={}, goods_type=goods_type)
        # 司机信息
        ids = '(%s)' % ', '.join([str(i) for i in set(dispatcher_nearby)])
        vehicle = CityNearbyCarsModel.get_driver(db.read_db, ids)
        if not vehicle:
            return Response(data={}, goods_type=goods_type)
        # 常驻地
        driver_ids = [i['user_id'] for i in vehicle]
        ids = '(%s)' % ', '.join([str(i) for i in set(driver_ids)])
        usual_regions = CityNearbyCarsModel.get_usual_region(db.read_bi, ids)
        for i in vehicle:
            usual_region = [j for j in usual_regions if j['user_id'] == i['user_id']]
            if usual_region:
                i['usual_province_id'] = usual_region[0]['from_province_id']
                i['usual_city_id'] = usual_region[0]['from_city_id']
                i['usual_county_id'] = usual_region[0]['from_county_id']
            else:
                i['usual_province_id'] = i['usual_city_id'] = i['usual_county_id'] = 0

        return Response(data={'goods': goods, 'vehicle': vehicle}, goods_type=goods_type)