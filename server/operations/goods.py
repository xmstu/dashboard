# -*- coding: utf-8 -*-
from server.database import db
from server.meta.decorators import make_decorator, Response
from server.models.goods import GoodsList, CancelReasonList, GoodsDistributionTrendList


class GoodsListDecorator(object):

    @staticmethod
    @make_decorator
    def get_goods_list(page, limit, params):
        goods_list = GoodsList.get_goods_list(db.read_db, page, limit, params)

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
