# -*- coding: utf-8 -*-
from server import log
from server.database import db
from server.meta.decorators import make_decorator, Response
from server.models.city import CityOrderListModel, CityResourceBalanceModel

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
        log.info('获取最新接单货源成功: [params: %s]' % (params))
        return Response(data=data)