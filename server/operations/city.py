
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
        return Response(goods=goods, vehicle=vehicle, params=params)




class CityOrderListDecorator(object):

    @staticmethod
    @make_decorator
    def get_data(page, limit, params):
        data = CityOrderListModel.get_data(db.read_db, page, limit, params)
        return Response(data=data)