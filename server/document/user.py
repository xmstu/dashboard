#!/usr/bin/python
# -*- coding:utf-8 -*-
# author=hexm

from flask_restplus import fields
from server.status import APIStatus, FeedAPIStatus
from server import api

request_user_list_param = api.doc(params={
    'user_name': '用户名',
    'mobile': '手机号',
    'reference_mobile': '推荐人手机',
    'download_channel': '下载渠道',
    'from_channel': '注册渠道',
    'is_referenced': '推荐注册',
    'home_station_id': '常驻地',
    'role_type': '注册角色',
    'role_auth': '认证角色',
    'is_actived': '是否活跃',
    'is_used': '操作过',
    'is_car_sticker': '贴车贴',
    'last_login_start_time': '最后登录开始时间',
    'last_login_end_time': '最后登录结束时间',
    'register_start_time': '注册开始时间',
    'register_end_time': '注册结束时间',
    'page': '页数',
    'limit': '条数'
    }, description='用户统计列表查询参数')

response_user_list_param_success = response_success = api.response(200, '成功', api.model('response_success', {
    'state': fields.Integer(description=str(APIStatus.Ok)),
    'msg': fields.String(description=FeedAPIStatus.Decriptions[APIStatus.Ok]),
}))