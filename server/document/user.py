#!/usr/bin/python
# -*- coding:utf-8 -*-
# author=hexm

from flask_restplus import fields
from server.status import APIStatus, FeedAPIStatus
from server import api

request_user_list_param = api.doc(params={
    'user_name': '用户名,默认:空',
    'mobile': '手机号,默认:空',
    'reference_mobile': '推荐人手机,默认:空',
    'download_channel': '下载渠道,默认:空',
    'from_channel': '注册渠道,默认:空',
    'is_referenced': '推荐注册,0:全部,1:有,2:无,默认:0',
    'region_id': '常驻地,	0:全部,其他地区用行政代码,默认:0',
    'role_type': '注册角色,0:全部,1:货主,2:司机,3:物流公司,默认:0',
    'role_auth': '认证角色,0:全部,1:货主,2:司机,3:物流公司,默认:0',
    'is_actived': '是否活跃,0:全部,1:活跃(连续登录天数>1),2:一般(1-3天未登录),3:即将沉睡(4-10天未登录),4:沉睡(10天以上未登录),默认:0',
    'is_used': '操作过,0:全部,1:发布货源,2:接单,3:完成订单,默认:0',
    'is_car_sticker': '贴车贴,0:全部,1:有,2:无,默认:0',
    'last_login_start_time': '最后登录开始时间',
    'last_login_end_time': '最后登录结束时间',
    'register_start_time': '注册开始时间',
    'register_end_time': '注册结束时间',
    'page': '页数',
    'limit': '条数'
    }, description='用户统计列表查询参数')

request_user_statistic_param = api.doc(params={
    'start_time': '开始日期(时间戳),默认:8天前',
    'end_time': '结束日期(时间戳),默认:昨天',
    'periods': '时间周期,2:日，3:周，4:月，默认:2',
    'user_type': '用户类型,1:新增用户,2:累计用户,默认:1',
    'role_type': '角色类型,0:全部,1:货主,2:司机,3:物流公司,默认:0',
    'region_id': '地区id,0:全部,其他地区用行政代码(模板写入),默认:0',
    'is_auth': '认证,0:全部,1:认证,2:非认证,默认:0',
    }, description='用户变化趋势查询参数')
