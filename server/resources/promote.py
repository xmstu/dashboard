#!/usr/bin/python
# -*- coding:utf-8 -*-
# author=hexm
from flask_restplus.resource import Resource
from flask import session
from flask_restful import abort

import server.document.promote as doc
import server.verify.general as general_verify
from server.status import HTTPStatus, make_result, APIStatus
from server import api
from server import verify, operations, filters
from server.meta.decorators import Response
from server.utils.request import get_all_arg, get_arg_int, get_arg, get_payload
from server.meta.session_operation import sessionOperationClass

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
    @filters.PromoteEffect.get_result(result=list, count=int, params=dict)
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
    @operations.PromoteEffectDecorator.add_extension_worker(user_id=int, mobile=str, user_name=str)
    @verify.PromoteEffect.check_add_params(role=int, user_id=int, payload=dict)
    def post():
        """新增推广人员"""
        role, user_id = sessionOperationClass.get_role()
        payload = get_payload()
        return Response(role=role, user_id=user_id, payload=payload)

class PromoteDelete(Resource):
    @staticmethod
    @doc.response_promote_effect_delete_param_success
    @filters.PromoteEffect.get_delete_data(result=int)
    @operations.PromoteEffectDecorator.delete_promoter(user_id=int, promoter_id=int)
    @verify.PromoteEffect.check_delete_params(role=int, user_id=int, promoter_id=int)
    def delete(id):
        """删除推广人员"""
        role, user_id = sessionOperationClass.get_role()
        promoter_id = id
        return Response(role=role, user_id=user_id, promoter_id=promoter_id)



ns = api.namespace('promote', description='推广统计')
ns.add_resource(PromoteQuality, '/quality/')
ns.add_resource(PromoteEffect, '/effect/')
ns.add_resource(PromoteDelete, '/effect/<int:id>')
