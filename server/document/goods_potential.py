#!/usr/bin/python
# -*- coding:utf-8 -*-
# author=hexm

from flask_restplus import fields

from server import api
from server.status import APIStatus, FeedAPIStatus

request_goods_potential_list_param = api.doc(params={
    'from_province_id': '发出地省份',
    'from_city_id': '发出地城市',
    'from_county_id': '发出地区县',
    'to_province_id': '目的地省份',
    'to_city_id': '目的地城市',
    'to_county_id': '目的地区县',
    'goods_type': '货源距离类型',
    'business': '货源业务类型',
    'haul_dist': '货源距离类型',
    'vehicle_name': '车长要求',
    'special_tag': '特殊要求',
    'register_start_time': '注册开始时间',
    'register_end_time': '注册结束时间',
    'record_start_time': '记录开始时间',
    'record_end_time': '记录结束时间',
    'page': '页数',
    'limit': '条数',
}, description='货源统计列表查询参数')

response_success = api.response(200, '成功', api.model('response_success', {
    'state': fields.Integer(description=str(APIStatus.Ok)),
    'msg': fields.String(description=FeedAPIStatus.Decriptions[APIStatus.Ok]),
}))


request_goods_distribution_trend_param = api.doc(params={
    'start_time': '开始时间',
    'end_time': '结束时间',
    'periods': '时间周期,2:日，3:周，4:月，默认:2',
    'goods_type': '货源类型',
    'goods_price_type': '货源类型,1:议价,2:一口价,默认:0全部',
    'region_id': '地区id',
    'payment_method': '0:全部;1.发货人付;2.收货人付;3.省心保',
}, description='货源分布趋势查询参数')