#!/usr/bin/python
# -*- coding:utf-8 -*-
# author=hexm
from flask_restplus.resource import Resource

import server.document.promote as doc
import server.verify.general as general_verify
from server import api
from server import verify, operations, filters
from server.meta.decorators import Response
from server.utils.request import get_all_arg, get_arg_int, get_payload


class PromoteEffect(Resource):

    @staticmethod
    @doc.request_promote_effect_param
    @doc.response_promote_effect_param_success
    @filters.PromoteEffect.get_result(data=dict)
    @operations.PromoteEffectDecorator.get_promote_effect_list(page=int, limit=int, params=dict)
    @verify.PromoteEffect.check_params(page=int, limit=int, params=dict)
    @general_verify.Paging.check_paging(page=int, limit=int, params=dict)
    def get():
        """获取参数"""
        resp = Response(
            page=get_arg_int('page', 1),
            limit=get_arg_int('limit', 10),
            params=get_all_arg()
        )

        return resp

    @staticmethod
    def post():
        """新增推广人员"""
        payload = get_payload()
        mobile = payload.get('mobile', None) or ''

        return Response(mobile=mobile)

    @staticmethod
    def delete():
        """删除推广人员"""
        payload = get_payload()
        reference_id = payload.get('reference_id', None) or 0

        return Response(reference_id=reference_id)


class PromoteQuality(Resource):
    @staticmethod
    @doc.request_promote_quality_param
    @doc.response_promote_quality_param_success
    @filters.PromoteQuality.get_result(params=dict, data=list, before_promote_count=int)
    @operations.PromoteQualityDecorator.get_promote_quality(params=dict)
    @verify.PromoteQuality.check_params(params=dict)
    def get():
        """获取参数"""
        resp = Response(params=get_all_arg())

        return resp


ns = api.namespace('promote', description='推广统计')
ns.add_resource(PromoteQuality, '/quality/')
ns.add_resource(PromoteEffect, '/effect/')
