#!/usr/bin/python
# -*- coding:utf-8 -*-
# author=hexm

from server import api

request_goods_potential_list_param = api.doc(params={
    'from_province_id': '发出地省份',
    'from_city_id': '发出地城市',
    'from_county_id': '发出地区县',
    'to_province_id': '目的地省份',
    'to_city_id': '目的地城市',
    'to_county_id': '目的地区县',
    'goods_price_type': '货源价格类型,1:一口价,2:议价,默认:0全部',
    'business': '货源业务类型:0.全部;1.整车;2.零担',
    'haul_dist': '货源距离类型:0.全部;1.同城;2.跨城',
    'vehicle_name': '车长要求',
    'special_tag': '特殊要求:0.全部;1.新注册;2.发过货;3.完成过订单;4.没完成过订单',
    'register_start_time': '注册开始时间',
    'register_end_time': '注册结束时间',
    'record_start_time': '记录开始时间',
    'record_end_time': '记录结束时间',
    'page': '页数',
    'limit': '条数',
}, description='潜在货源统计列表查询参数')


request_goods_potential_distribution_trend_param = api.doc(params={
    'start_time': '开始时间',
    'end_time': '结束时间',
    'periods': '时间周期,2:日，3:周，4:月，默认:2',
    'goods_price_type': '货源价格类型,1:一口价,2:议价,默认:0全部',
    'business': '货源业务类型:0.全部;1.整车;2.零担',
    'haul_dist': '货源距离类型:0.全部;1.同城;2.跨城',
    'region_id': '地区id',
}, description='潜在货源分布趋势查询参数')