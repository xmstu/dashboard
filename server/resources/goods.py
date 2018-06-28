# -*- coding: utf-8 -*-
from flask_restplus import Resource

import server.verify.general as general_verify
import server.document.goods as doc
from server import log, verify, operations, filters, api
from server.meta.decorators import Response
from server.utils.request import get_all_arg, get_arg_int


class GoodsList(Resource):

    @staticmethod
    @doc.request_goods_list_param
    @filters.GoodsList.get_result(data=dict)
    @operations.GoodsListDecorator.get_goods_list(page=int, limit=int, params=dict)
    @verify.GoodsList.check_params(page=int, limit=int, params=dict)
    @general_verify.Paging.check_paging(page=int, limit=int, params=dict)
    def get():
        """货源列表"""
        resp = Response(
            page=get_arg_int('page', 1),
            limit=get_arg_int('limit', 10),
            params=get_all_arg())

        log.debug('获取货源列表请求参数{}'.format(resp))
        return resp


class CancelGoodsReason(Resource):
    @staticmethod
    @doc.request_cancel_reason_param
    @filters.CancelGoodsReason.get_result(data=dict)
    @operations.CancelGoodsReason.get_cancel_reason_list(params=dict)
    @verify.CancelGoodsReason.check_params(params=dict)
    def get():
        """取消货源原因"""
        resp = Response(params=get_all_arg())

        return resp

class GoodsDistributionTrend(Resource):

    @staticmethod
    @doc.request_goods_distribution_trend_param
    @filters.GoodsDistributionTrend.get_result(data=dict, params=dict)
    @operations.GoodsDistributionTrend.get_goods_distribution_trend(params=dict)
    @verify.GoodsDistributionTrend.check_params(params=dict)
    def get():
        """货源分布趋势"""
        resp = Response(params=get_all_arg())

        return resp


ns = api.namespace('goods', description='货源统计')
ns.add_resource(GoodsList, '/list/')
ns.add_resource(CancelGoodsReason, '/cancel/')
ns.add_resource(GoodsDistributionTrend, '/goods_distribution_trend/')

