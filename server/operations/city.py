# -*- coding: utf-8 -*-
from server import log
from server.database import db
from server.meta.decorators import make_decorator, Response
from server.models.city import CityOrderListModel, CityResourceBalanceModel, CityNearbyCarsModel
from server.mysqldb import MongoLinks
from server.configs import configs

import datetime
from decimal import Decimal

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
            # 新建mongo连接, 省内存
            user_locations = MongoLinks(config=dict(configs.remote.union.mongo.locations.get()), collection='user_locations')
            # 货源5公里内用户
            user_location = user_locations.collection.aggregate([
                {'$geoNear': {
                    'near': [float(goods['from_longitude']), float(goods['from_latitude'])],
                    'maxDistance': 5000,
                    'distanceField': 'distance',
                    'spherical': True
                }},
                {'$match': {
                    'time': {'$gt':  datetime.datetime.today() - datetime.timedelta(days=1)},
                    'province_id': goods['from_province_id'],
                    'city_id': goods['from_city_id'],
                    'county_id': goods['from_county_id']
                 }},
                 {'$group': {'_id': '$user_id', 'time': {'$max': '$time'}}}
            ])
            user_location = [(i['_id'], i['time']) for i in user_location]
            if not user_location:
                return Response(data={}, goods_type=goods_type)
            # 获取用户信息
            locations = {}
            for i in user_location:
                result = user_locations.collection.find({
                    'time': i[1],
                    'user_id': i[0],
                }, {'user_id': 1, 'time': 1, 'address': 1, 'longitude': 1, 'latitude': 1}).limit(1)
                result = [j for j in result]
                locations[i[0]] = result[0] if result else {
                    'address': '',
                    'longitude': 0,
                    'latitude': 0,
                    'time': 0
                }

            # 1.附近车辆-常驻地
            if goods_type == 1:
                driver = CityNearbyCarsModel.get_usual_region(db.read_bi,
                                                                    goods['from_city_id'],
                                                                    goods['from_county_id'],
                                                                    [str(i) for i in locations])
                driver_id = [str(i['user_id']) for i in driver]
                if not driver_id:
                    pass
                else:
                    driver_info = CityNearbyCarsModel.get_driver_info(db.read_db, driver_id)
                    if driver_info:
                        for i in driver:
                            result = [j for j in driver_info if j['user_id'] == i['user_id']]
                            if result:
                                i.update(result[0])
            # 2.附近车辆-接单线路
            else:
                driver = CityNearbyCarsModel.get_driver_by_booking(db.read_db, goods_id, [str(i) for i in locations])
            if not driver:
                return Response(data={}, goods_type=goods_type)
            for i in driver:
                if locations.get(i.get('user_id', 0)):
                    i['locations'] = locations[i['user_id']]
                else:
                    i['locations'] = {
                        'address': '',
                        'longitude': 0,
                        'latitude': 0,
                        'time': 0
                    }

            return Response(data={'goods': goods, 'driver': driver}, goods_type=goods_type)
        except Exception as e:
            log.error('获取货源附近车辆报错: [error: %s]' % e, exc_info=True)