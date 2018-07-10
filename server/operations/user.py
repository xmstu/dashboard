# -*- coding: utf-8 -*-

from flask_restful import abort

from server.meta.decorators import make_decorator, Response
from server.models.user import UserList,UserStatistic
from server.database import db


class UserListDecorator(object):

    @staticmethod
    @make_decorator
    def get_user_list(page, limit, params):
        # 用户详情
        user_list = UserList.get_user_list(db.read_bi, page, limit, params)
        company_auth = set(["'"+str(i['user_id'])+"'" for i in user_list['user_detail'] if i.get('company_auth', 0) == 1 and i.get('user_id', 0) != 0])
        # 认证公司名称替换用户名
        if company_auth:
            user_ids = ','.join(company_auth)
            result = UserList.get_company_name(db.read_db, user_ids)
            company_name = {}
            for i in result:
                company_name[i['user_id']] = i['company_name']

            for i in user_list['user_detail']:
                if company_name.get(i['user_id']):
                    i['user_name'] = company_name[i['user_id']]

        return Response(user_list=user_list)


class UserStatisticDecorator(object):

    @staticmethod
    @make_decorator
    def get_user_statistic(params):
        """用户变化趋势统计"""
        # 用户常驻地
        user_ids = None
        if params['region_id']:
            # 用户自选
            if isinstance(params['region_id'], int):
                user_ids = UserList.get_user_home_station_by_int(db.read_bi, params['region_id'])
            # 非管理员默认地区
            elif isinstance(params['region_id'], list):
                user_ids = UserList.get_user_home_station_by_list(db.read_bi, params['region_id'])

        user_statistic = UserStatistic.get_user_statistic_by_mobile(db.read_db, params, user_ids)
        before_user_count = 0
        if params['user_type'] == 2:
            before_user_count = UserStatistic.get_before_user_count_by_mobile(db.read_db, params, user_ids)
        return Response(params=params, data=user_statistic, before_user_count=before_user_count)

