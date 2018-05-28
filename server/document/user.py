#!/usr/bin/python
# -*- coding:utf-8 -*-
# author=hexm

from flask_restplus import fields
from server.status import APIStatus, FeedAPIStatus
from server import api

request_user_list_param = api.doc(body=api.model('request_user_list_param', {
    'user_name': fields.String(description='用户名'),
    'mobile': fields.String(description='手机号'),
    'reference_mobile': fields.String(description='推荐人手机'),
    'download_channel': fields.String(description='下载渠道'),
    'from_channel': fields.String(description='注册渠道'),
    'is_referenced': fields.String(description='推荐注册'),
    'home_station_id': fields.String(description='常驻地'),
    'role_type': fields.String(description='注册角色'),
    'role_auth': fields.String(description='认证角色'),
    'is_actived': fields.String(description='是否活跃'),
    'is_used': fields.String(description='操作过'),
    'is_car_sticker': fields.String(description='贴车贴'),
    'index': fields.String(description='页数'),
    'count': fields.String(description='条数'),
    }, description='用户统计列表查询参数')
)

response_user_list_param_success = response_success = api.response(200, '成功', api.model('response_success', {
    'state': fields.Integer(description=str(APIStatus.Ok)),
    'msg': fields.String(description=FeedAPIStatus.Decriptions[APIStatus.Ok]),
}))