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
    @doc.response_goods_list_param_success
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

        log.info('resp:{}'.format(resp))
        return resp


ns = api.namespace('goods', description='货源统计')
ns.add_resource(GoodsList, '/list/')

