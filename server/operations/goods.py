# -*- coding: utf-8 -*-
from server.database import db
from server.meta.decorators import make_decorator, Response
from server.models.goods import GoodsList, CancelReasonList, GoodsDistributionTrendList, FreshConsignor


class GoodsListDecorator(object):

    @staticmethod
    @make_decorator
    def get_goods_list(page, limit, params):
        if params.get('new_goods_type') == 1:
            user_id_list = FreshConsignor.get_user_id_list(db.read_db, params.get('node_id'))
        else:
            user_id_list = ['0']

        goods_list = GoodsList.get_goods_list(db.read_db, page, limit, user_id_list, params)

        return Response(data=goods_list)


class CancelGoodsReason(object):

    @staticmethod
    @make_decorator
    def get_cancel_reason_list(params):
        cancel_reason_list = CancelReasonList.get_cancel_reason_list(db.read_db, params)

        return Response(data=cancel_reason_list)


class GoodsDistributionTrend(object):

    @staticmethod
    @make_decorator
    def get_goods_distribution_trend(params):
        goods_distribution_trend = GoodsDistributionTrendList.get_goods_distribution_trend(db.read_db, params)

        return Response(data=goods_distribution_trend, params=params)
