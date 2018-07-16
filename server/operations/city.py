# -*- coding: utf-8 -*-
from server import log
from server.database import db
from server.meta.decorators import make_decorator, Response
from server.models.city import CityOrderListModel, CityResourceBalanceModel, CityNearbyCarsModel
from server.models.vehicle import VehicleModel
from server.database import pyredis
from server.utils.amap import distance

import time

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
            # 1.附近车辆-常驻地
            if goods_type == 2:
                all_drivers = CityNearbyCarsModel.get_all_drivers(db.read_bi, goods['from_province_id'], goods['from_city_id'])
                driver = []
                for i in all_drivers:
                    result = pyredis.token.read_one('online:position:%s' % i['user_id'])
                    last_delta = int(time.time() - time.mktime(time.strptime(result['location_time'], '%Y-%m-%d %H:%M:%S')))
                    if result and result['county'] == goods['from_county_id'] and last_delta < 86400:
                        # 订单、车长数据
                        length_id = str(i['vehicle_length_id']).split(',')[0]
                        user_info = VehicleModel.get_vehicle_length_name(db.read_db, int(length_id), i['user_id'])
                        if int(goods['inner_length']) > int(user_info['value']):
                            continue
                        i.update({
                            'address': result['address'],
                            'longitude': result['longitude'],
                            'latitude': result['latitude'],
                            'last_login_time': result['location_time'],
                            'last_delta': last_delta,
                            'province': result['province'],
                            'city': result['city'],
                            'county': result['county'],
                            'order_count': user_info['order_count'],
                            'order_finished': user_info['order_finished'],
                            'order_cancel': user_info['order_cancel']
                        })
                        driver.append(i)
                    if len(driver) >= 10:
                        break
            # 2.附近车辆-接单线路
            else:
                driver = CityNearbyCarsModel.get_driver_by_booking(db.read_db, goods_id)
            if not driver:
                return Response(data={}, goods_type=goods_type)

            return Response(data={'goods': goods, 'driver': driver}, goods_type=goods_type)
        except Exception as e:
            log.error('获取货源附近车辆报错: [error: %s]' % e, exc_info=True)