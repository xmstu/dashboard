# -*- coding: utf-8 -*-
from server import log
from server.database import db
from server.meta.decorators import make_decorator, Response
from server.models.city import CityOrderListModel, CityResourceBalanceModel, CityNearbyCarsModel
from server.models.vehicle import VehicleModel
from server.database import pyredis
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
            # 1.附近车辆-附近货车
            if goods_type == 2:
                all_drivers = CityNearbyCarsModel.get_all_drivers(db.read_bi, goods['from_province_id'], goods['from_city_id'])
                driver = []
                today = time.mktime(time.strptime(time.strftime('%Y-%m-%d 00:00:00', time.localtime(time.time())),'%Y-%m-%d %H:%M:%S'))
                for i in all_drivers:
                    result = pyredis.token.read_one('online:position:%s' % i['user_id'])
                    if result and result['province'] == goods['from_province_id'] \
                    and result['city'] == goods['from_city_id'] \
                    and result['county'] == goods['from_county_id'] \
                    and today - time.mktime(time.strptime(result['location_time'], '%Y-%m-%d %H:%M:%S')) > 86400:
                        # 车长
                        length_id = str(i['vehicle_length_id']).split(',')[0]
                        i['vehicle_length_id'] = VehicleModel.get_vehicle_length_name(db.read_db, int(length_id))
                        i.update({
                            'address': result['address'],
                            'longitude': result['longitude'],
                            'latitude': result['latitude'],
                            'last_login_time': result['location_time'],
                            'last_delta': today - time.mktime(time.strptime(result['location_time'], '%Y-%m-%d %H:%M:%S')),
                            'province': result['province'],
                            'city': result['city'],
                            'county': result['county']
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