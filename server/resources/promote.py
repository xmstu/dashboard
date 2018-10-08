#!/usr/bin/python
# -*- coding:utf-8 -*-
# author=hexm
from flask_restplus.resource import Resource

import server.document.promote as doc
import server.verify.general as general_verify
from server import api
from server import verify, operations, filters
from server.meta.decorators import Response
from server.meta.session_operation import SessionOperationClass
from server.utils.request import get_all_arg, get_arg_int, get_payload


class PromoteQuality(Resource):
    @staticmethod
    @doc.request_promote_quality_param
    @doc.response_promote_quality_param_success
    @filters.PromoteQuality.get_result(params=dict, data=list, before_promote_count=int)
    @operations.PromoteQualityDecorator.get_promote_quality(params=dict)
    @verify.PromoteQuality.check_params(params=dict)
    def get():
        """推广数据统计"""
        resp = Response(params=get_all_arg())
        return resp


class PromoteEffect(Resource):

    @staticmethod
    @doc.request_promote_effect_param
    @doc.response_promote_effect_param_success
    @operations.PromoteEffectDecorator.get_promote_effect_list(page=int, limit=int, params=dict)
    @verify.PromoteEffect.check_params(page=int, limit=int, params=dict)
    @general_verify.Paging.check_paging(page=int, limit=int, params=dict)
    def get():
        """推荐人员列表"""
        resp = Response(
            page=get_arg_int('page', 1),
            limit=get_arg_int('limit', 10),
            params=get_all_arg()
        )

        return resp

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
    @verify.PromoteEffect.check_delete_params(role_type=int, user_id=int, promoter_mobile=str)
    def delete(mobile):
        """删除推广人员"""
        role_type, user_id = SessionOperationClass.get_role()
        promoter_mobile = mobile
        return Response(role_type=role_type, user_id=user_id, promoter_mobile=promoter_mobile)


ns = api.namespace('promote', description='推广统计')
ns.add_resource(PromoteQuality, '/quality/')
ns.add_resource(PromoteEffect, '/effect/')
ns.add_resource(PromoteDelete, '/effect/<string:mobile>')
