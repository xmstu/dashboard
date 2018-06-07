#!/usr/bin/python
# -*- coding:utf-8 -*-
# author=hexm

from flask_restplus import fields
from server.status import APIStatus, FeedAPIStatus
from server import api

request_promote_effect_param = api.doc(params={
    'user_name': '用户名',
    'mobile': '手机号',
    'region_id': '所属地区',
    'role_type': '推荐人角色',
    'goods_type': '货源类型',
    'is_actived': '是否活跃',
    'is_car_sticker': '贴车贴',
    'start_time':'新增日期开始时间',
    'end_time':'新增日期结束时间',
    'page': '页数',
    'limit': '条数'
    }, description='推广统计列表查询参数')

response_promote_effect_param_success = response_success = api.response(200, '成功', api.model('response_success', {
    'state': fields.Integer(description=str(APIStatus.Ok)),
    'msg': fields.String(description=FeedAPIStatus.Decriptions[APIStatus.Ok]),
}))

request_promote_quality_param = api.doc(params={
    'start_time':'开始日期(时间戳)',
    'end_time':'结束日期(时间戳)',
    'periods':'时间周期',
    'dimension':'统计维度',
    'data_type':'数据类型',
    }, description='推广统计列表查询参数')

response_promote_quality_param_success = api.response(200, '成功', api.model('response_success', {
    'state': fields.Integer(description=str(APIStatus.Ok)),
    'msg': fields.String(description=FeedAPIStatus.Decriptions[APIStatus.Ok]),
}))
