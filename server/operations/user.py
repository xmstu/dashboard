# -*- coding: utf-8 -*-

from flask_restful import abort

from server import log
from server.meta.decorators import make_decorator, Response
from server.models.user import UserList,UserStatistic
from server.database import db
from server.status import HTTPStatus, make_resp, APIStatus


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

    @staticmethod
    @make_decorator
    def get_user_behavior_statistic(params):
        """用户行为趋势变化统计"""
        try:
            # 发货人数
            if params["data_type"] == 1:
                data = UserStatistic.get_consignor(db.read_db, params)
            # 新增发货人数
            elif params["data_type"] == 2:
                data = UserStatistic.get_new_consignor(db.read_db, params)
            # 流失货主人数
            elif params["data_type"] == 3:
                data = UserStatistic.get_lost_consignor(db.read_db, params)
            # 接单司机人数/完成订单司机数
            elif params["data_type"] in (4, 5):
                data = UserStatistic.get_driver(db.read_db, params)
            # 新增接单人数
            elif params["data_type"] == 6:
                data = UserStatistic.get_new_driver(db.read_db, params)
            # 流失司机人数
            elif params["data_type"] == 7:
                data = UserStatistic.get_lost_driver(db.read_db, params)
            else:
                data = []
            return Response(params=params, data=data)
        except Exception as e:
            log.error('查询用户行为趋势出现错误 [Error: %s]' % e)
            abort(HTTPStatus.InternalServerError, **make_resp(status=APIStatus.InternalServerError, msg='查询用户行为趋势出现错误'))

