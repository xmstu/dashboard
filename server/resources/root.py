#!/usr/bin/python
# -*- coding:utf-8 -*-
# author=hexm

from flask_restplus.resource import Resource

import server.document.root as doc
from server import api
from server import verify, operations, filters
from server.meta.decorators import Response
from server.utils.request import *


class RootManagement(Resource):
    @staticmethod
    @doc.request_root_management_get
    @filters.RootManagement.get_result(params=dict, data=list, before_user_count=int)
    @operations.RootManagement.get_data(params=dict)
    @verify.RootManagement.check_get_params(params=dict)
    def get():
        """超级用户管理列表"""
        resp = Response(params=get_all_arg())

        return resp

    @staticmethod
    @doc.request_root_management_add
    @operations.RootManagement.add_data(params=dict)
    @verify.RootManagement.check_add_params(params=dict)
    def add():
        """增加新的城市经理或合伙人"""
        pass

    @staticmethod
    @operations.RootManagement.delete_data(params=dict)
    def delete(id):
        """删除该账户"""
        pass

    @staticmethod
    @doc.request_root_management_put
    @operations.RootManagement.put_data(params=dict)
    @verify.RootManagement.check_put_params(params=dict)
    def put(id):
        """修改当前用户id的账号或者密码"""
        pass


ns = api.namespace('root', description='超级用户管理')
ns.add_resource(RootManagement, '/management/')
