# -*- coding: utf-8 -*-
from server import log
from server.database import db, pyredis
from server.meta.decorators import make_decorator, Response
from server.models.city import CityOrderListModel, CityResourceBalanceModel, CityNearbyCarsModel
from server.mysqldb import MongoLinks
from server.configs import configs


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
            usual_driver = CityNearbyCarsModel.get_usual_region(db.read_bi, goods['from_city_id'], goods['from_county_id'])
            driver_id = [str(i['user_id']) for i in usual_driver]
            if not driver_id:
                pass
            else:
                driver_info = CityNearbyCarsModel.get_driver_info(db.read_db, driver_id)
                if driver_info:
                    for i in usual_driver:
                        result = [j for j in driver_info if j['user_id'] == i['user_id']]
                        if result:
                            i.update(result[0])
            # 2.附近车辆-接单线路
            booking_driver = CityNearbyCarsModel.get_driver_by_booking(db.read_db, goods_id)

            driver = usual_driver + booking_driver

            # 司机定位, 新建mongodb连接
            driver_id = [i.get('user_id') for i in driver]
            user_locations = MongoLinks(config=dict(configs.remote.union.mongo.locations.get()), collection='user_locations')
            locations = {}
            for i in set(driver_id):
                result = user_locations.collection.find(
                    {'user_id': i},
                    {'province_name': 1, 'city_name': 1, 'county_name': 1, 'address': 1, 'longitude': 1, 'latitude': 1, 'user_id': 1}
                ).sort([('_id', -1)]).limit(1)
                result = [j for j in result]
                locations[i] = result[0] if result else {
                        'province_name': '',
                        'city_name': '',
                        'county_name': '',
                        'address': '',
                        'longitude': 0,
                        'latitude': 0
                    }

            for i in driver:
                if locations.get(i.get('user_id', 0)):
                    i['locations'] = locations[i['user_id']]
                else:
                    i['locations'] = {
                        'province_name': '',
                        'city_name': '',
                        'county_name': '',
                        'address': '',
                        'longitude': 0,
                        'latitude': 0
                    }


            return Response(data={'goods': goods, 'driver': driver}, goods_type=goods_type)
        except Exception as e:
            log.error('获取货源附近车辆报错: [error: %s]' % e, exc_info=True)