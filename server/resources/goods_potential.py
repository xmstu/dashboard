# -*- coding: utf-8 -*-
from flask_restplus import Resource

import server.verify.general as general_verify
import server.document.goods_potential as doc
from server import log, verify, operations, filters, api
from server.meta.decorators import Response
from server.utils.request import get_all_arg, get_arg_int


class GoodsPotentialDistributionTrend(Resource):

    @staticmethod
    @doc.request_goods_potential_distribution_trend_param
    @filters.GoodsPotentialDistributionTrend.get_result(data=dict, params=dict)
    @operations.GoodsPotentialDistributionTrend.get_goods_potential_distribution_trend(params=dict)
    @verify.GoodsPotentialDistributionTrend.check_params(params=dict)
    def get():
        """潜在货源分布趋势"""
        resp = Response(params=get_all_arg())

        return resp


class GoodsPotentialList(Resource):

    @staticmethod
    @doc.request_goods_potential_list_param
    @filters.GoodsPotentialList.get_result(data=dict)
    @operations.GoodsPotentialList.get_potential_goods_list(page=int, limit=int, params=dict)
    @verify.GoodsPotentialList.check_params(page=int, limit=int, params=dict)
    @general_verify.Paging.check_paging(page=int, limit=int, params=dict)
    def get():
        """潜在货源列表"""
        resp = Response(
            page=get_arg_int('page', 1),
            limit=get_arg_int('limit', 10),
            params=get_all_arg())

        log.debug('获取潜在货源列表请求参数{}'.format(resp))
        return resp


ns = api.namespace('goods_potential', description='潜在货源统计')
ns.add_resource(GoodsPotentialList, '/list/')

