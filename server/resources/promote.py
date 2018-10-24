#!/usr/bin/python
# -*- coding:utf-8 -*-
# author=hexm
from flask_restplus.resource import Resource

import server.document.promote as doc
from server import api
from server import verify, operations, filters
from server.filters import promote_quality_get_result
from server.meta.decorators import Response
from server.meta.redis_cache import redis_cache
from server.meta.session_operation import SessionOperationClass
from server.operations import get_promote_quality, get_promote_effect_list
from server.utils.request import get_all_arg, get_payload
from server.verify import promote_quality_check_params, promote_effect_check_params


class PromoteQuality(Resource):
    @staticmethod
    @doc.request_promote_quality_param
    @redis_cache(expire_time=86400)
    def get():
        """推广数据统计"""
        params = promote_quality_check_params(params=get_all_arg())
        promote_quality, before_promote_count = get_promote_quality(params)
        return promote_quality_get_result(params, promote_quality, before_promote_count)


class PromoteEffect(Resource):

    @staticmethod
    @doc.request_promote_effect_param
    @doc.response_promote_effect_param_success
    @redis_cache(expire_time=86400)
    def get():
        """推荐人员列表"""
        params = promote_effect_check_params(params=get_all_arg())
        return get_promote_effect_list(params)

    @staticmethod
    @doc.request_promote_effect_add_param
    @doc.response_promote_effect_add_param_success
    @filters.PromoteEffect.get_add_data(result=int)
    @operations.PromoteEffectDecorator.add_extension_worker(params=dict)
    @verify.PromoteEffect.check_add_params(role_type=int, user_id=int, payload=dict)
    def post():
        """新增推广人员"""
        role_type, user_id = SessionOperationClass.get_role()
        payload = get_payload()
        return Response(role_type=role_type, user_id=user_id, payload=payload)


class PromoteDelete(Resource):
    @staticmethod
    @doc.response_promote_effect_delete_param_success
    @filters.PromoteEffect.get_delete_data(result=int)
    @operations.PromoteEffectDecorator.delete_promoter(params=dict)
    @verify.PromoteEffect.check_delete_params(role_type=int, promoter_mobile=str)
    def delete(mobile):
        """删除推广人员"""
        role_type, _ = SessionOperationClass.get_role()
        promoter_mobile = mobile
        return Response(role_type=role_type, promoter_mobile=promoter_mobile)


ns = api.namespace('promote', description='推广统计')
ns.add_resource(PromoteQuality, '/quality/')
ns.add_resource(PromoteEffect, '/effect/')
ns.add_resource(PromoteDelete, '/effect/<string:mobile>')
