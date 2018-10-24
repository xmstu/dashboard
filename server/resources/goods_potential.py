# -*- coding: utf-8 -*-
from flask_restplus import Resource

import server.document.goods_potential as doc
from server import log, api
from server.filters import goods_potential_distribution_trend_get_result, goods_potential_list_get_result
from server.meta.redis_cache import redis_cache
from server.operations import get_goods_potential_distribution_trend, get_potential_goods_list
from server.utils.request import get_all_arg
from server.verify import goods_potential_distribution_trend_check_params, goods_potential_list_check_params


class GoodsPotentialDistributionTrend(Resource):

    @staticmethod
    @doc.request_goods_potential_distribution_trend_param
    @redis_cache(expire_time=7200)
    def get():
        """潜在货源分布趋势"""
        params = goods_potential_distribution_trend_check_params(params=get_all_arg())
        data = get_goods_potential_distribution_trend(params)
        result = goods_potential_distribution_trend_get_result(data, params)
        return result


class GoodsPotentialList(Resource):

    @staticmethod
    @doc.request_goods_potential_list_param
    @redis_cache(expire_time=7200)
    def get():
        """潜在货源列表"""
        params = goods_potential_list_check_params(params=get_all_arg())
        log.debug('获取潜在货源列表请求参数{}'.format(params))
        data = get_potential_goods_list(params)
        result = goods_potential_list_get_result(data)
        return result


ns = api.namespace('potential', description='潜在货源统计')
ns.add_resource(GoodsPotentialList, '/list/')
ns.add_resource(GoodsPotentialDistributionTrend, '/trend/')
