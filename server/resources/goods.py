# -*- coding: utf-8 -*-
from flask_restplus import Resource

import server.document.goods as doc
from server import api, log
from server.filters import goods_list_get_result, goods_distribution_trend_get_result
from server.meta.redis_cache import redis_cache
from server.operations import get_goods_list, get_goods_cancel_reason_list, get_goods_distribution_trend
from server.utils.request import get_all_arg
from server.verify import goods_list_check_params, cancel_goods_reason_check_params, \
    goods_distribution_trend_check_params


class GoodsList(Resource):

    @doc.request_goods_list_param
    @redis_cache(expire_time=300)
    def get(self):
        """货源列表"""

        params = goods_list_check_params(params=get_all_arg())
        log.info("货源列表的查询参数: [params: {}]".format(params))
        goods_list = get_goods_list(params)
        result = goods_list_get_result(goods_list)

        return result


class CancelGoodsReason(Resource):

    @doc.request_cancel_reason_param
    @redis_cache(expire_time=7200)
    def get(self):
        """取消货源原因"""
        params = cancel_goods_reason_check_params(params=get_all_arg())
        log.info("取消货源原因的查询参数: [params: {}]".format(params))
        reason_list = get_goods_cancel_reason_list(params)

        return reason_list


class GoodsDistributionTrend(Resource):

    @doc.request_goods_distribution_trend_param
    @redis_cache(expire_time=7200)
    def get(self):
        """货源分布趋势"""
        params = goods_distribution_trend_check_params(params=get_all_arg())
        log.info("货源分布趋势的查询参数: [params: {}]".format(params))
        goods_distribution_trend = get_goods_distribution_trend(params)
        result = goods_distribution_trend_get_result(goods_distribution_trend, params)

        return result


ns = api.namespace('goods', description='货源统计')
ns.add_resource(GoodsList, '/list/')
ns.add_resource(CancelGoodsReason, '/cancel/')
ns.add_resource(GoodsDistributionTrend, '/goods_distribution_trend/')
