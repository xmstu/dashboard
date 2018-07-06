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

        return Response(goods=goods, vehicle=vehicle, params=params)


class CityOrderListDecorator(object):

    @staticmethod
    @make_decorator
    def get_data(page, limit, params):
        """最新接单货源"""
        data = CityOrderListModel.get_data(db.read_db, page, limit, params)

        return Response(data=data)


class CityNearbyCars(object):

    @staticmethod
    @make_decorator
    def get_data(goods_id, goods_type):
        """货源附近车辆"""
        try:
            # 获取货源信息
            goods = CityNearbyCarsModel.get_goods(db.read_db, goods_id)
            if not goods:
                return Response(data={}, goods_type=goods_type)
            # 附近车辆-司机定位
            nearby_vehicle = pyredis['nearby_vehicle']
            dispatcher_nearby = nearby_vehicle.read_georadius('dispatch.vehicle.nearby', goods['from_longitude'], goods['from_latitude'], 5, 'km')
            if not dispatcher_nearby:
                return Response(data={}, goods_type=goods_type)
            # 附近司机(限制10条)
            ids = '(%s)' % ', '.join([str(i) for i in set(dispatcher_nearby)])
            nearby_driver = CityNearbyCarsModel.get_driver_by_position(db.read_db, ids)
            if not nearby_driver:
                return Response(data={}, goods_type=goods_type)

            # 附近车辆-接单线路
            booking_driver = CityNearbyCarsModel.get_driver_by_booking(db.read_db, goods_id)

            driver = nearby_driver + booking_driver

            return Response(data={'goods': goods, 'driver': driver}, goods_type=goods_type)
        except Exception as e:
            log.error('获取货源附近车辆报错: [error: %s]' % e, exc_info=True)