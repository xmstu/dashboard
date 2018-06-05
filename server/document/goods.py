#!/usr/bin/python
# -*- coding:utf-8 -*-
# author=hexm

from flask_restplus import fields

from server import api
from server.status import APIStatus, FeedAPIStatus

request_goods_list_param = api.doc(params={
    'goods_id': '货源id',
    'mobile': '货主手机',
    'from_province_id': '发出地省份',
    'from_city_id': '发出地城市',
    'from_dist_id': '发出地区县',
    'to_province_id': '目的地省份',
    'to_city_id': '目的地城市',
    'to_dist_id': '目的地区县',
    'goods_type': '货源类型',
    'goods_status': '货源状态',
    'is_called': '是否通话',
    'vehicle_length': '车长要求',
    'vehicle_type': '车型要求',
    'node_id': '所属网点',
    'new_goods_type': '初次下单',
    'urgent_goods': '急需处理',
    'is_addition': '是否加价',
    'create_start_time': '发布开始日期',
    'create_end_time': '发布结束日期',
    'load_start_time': '装货开始日期',
    'load_end_time': '装货结束日期',
    'page': '页数',
    'limit': '条数',
}, description='货源统计列表查询参数')

response_goods_list_param_success = response_success = api.response(200, '成功', api.model('response_success', {
    'state': fields.Integer(description=str(APIStatus.Ok)),
    'msg': fields.String(description=FeedAPIStatus.Decriptions[APIStatus.Ok]),
}))
