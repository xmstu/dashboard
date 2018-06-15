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
from server.utils.request import get_all_arg, get_arg_int, get_arg


class PromoteEffect(Resource):

    @staticmethod
    @doc.request_promote_effect_param
    @doc.response_promote_effect_param_success
    @filters.PromoteEffect.get_result(extension_worker_list=dict, promote_effect_list=dict, params=dict)
    @operations.PromoteEffectDecorator.get_promote_effect_list(page=int, limit=int, params=dict)
    @verify.PromoteEffect.check_params(page=int, limit=int, params=dict)
    @general_verify.Paging.check_paging(page=int, limit=int, params=dict)
    def get():
        """推荐人员效果"""
        resp = Response(
            page=get_arg_int('page', 1),
            limit=get_arg_int('limit', 10),
            params=get_all_arg()
        )

        return resp

    @staticmethod
    @doc.request_promote_effect_add_param
    @doc.response_promote_effect_add_param_success
    @filters.PromoteEffect.get_add_data(data=int)
    @operations.PromoteEffectDecorator.add_extension_worker(user_id=int, mobile=str)
    @verify.PromoteEffect.check_add_params(user_id=int, mobile=str)
    def post():
        """新增推广人员"""
        if not session.get('login'):
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='未登录用户'))
        user_id = session['login'].get('user_id', 0)
        mobile = get_arg('mobile', '')
        return Response(user_id=user_id, mobile=mobile)

    @staticmethod
    @doc.request_promote_effect_delete_param
    @doc.response_promote_effect_delete_param_success
    @filters.PromoteEffect.get_delete_data(data=int)
    @operations.PromoteEffectDecorator.delete_from_tb_inf_promte(reference_id=int)
    @verify.PromoteEffect.check_delete_params(arg=dict)
    def delete():
        """删除推广人员"""
        arg = get_all_arg()

        return Response(arg=arg)


class PromoteQuality(Resource):
    @staticmethod
    @doc.request_promote_quality_param
    @doc.response_promote_quality_param_success
    @filters.PromoteQuality.get_result(params=dict, data=list, before_promote_count=int)
    @operations.PromoteQualityDecorator.get_promote_quality(params=dict)
    @verify.PromoteQuality.check_params(params=dict)
    def get():
        """推荐人质量"""
        resp = Response(params=get_all_arg())

        return resp


ns = api.namespace('promote', description='推广统计')
ns.add_resource(PromoteQuality, '/quality/')
ns.add_resource(PromoteEffect, '/effect/')
