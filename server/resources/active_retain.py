#!/usr/bin/python
# -*- coding:utf-8 -*-
# author=hexm

from flask_restplus.resource import Resource

import server.document.active_retain as doc
from server import api
from server import verify, operations, filters
from server.meta.decorators import Response
from server.utils.request import *


class ActiveUserStatistic(Resource):

    @staticmethod
    @doc.request_user_retain_statistic_param
    @filters.ActiveUserStatistic.get_active_user_statistic(params=dict, data=list)
    @operations.ActiveUserStatistic.get_active_user_statistic(params=dict)
    @verify.ActiveUserStatistic.check_params(params=dict)
    def get():
        """获取活跃用户趋势"""
        return Response(params=get_all_arg())


class ActiveUserList(Resource):

    @staticmethod
    @doc.request_user_retain_list_param
    def get():
        """获取留存统计表格"""
        return Response(params=get_all_arg())


ns = api.namespace('active_retain', description='活跃留存')
ns.add_resource(ActiveUserStatistic, '/statistic/')
ns.add_resource(ActiveUserList, '/list/')
