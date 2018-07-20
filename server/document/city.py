# -*- coding: utf-8 -*-

from server import api

request_city_resource_balance = api.doc(params={
    'start_time': '开始日期(时间戳),默认:8天前',
    'end_time': '结束日期(时间戳),默认:昨天',
    'region_id': '地区id,默认:0',
    'goods_type': '类型:1.同城,2.跨城,3.零担,默认:0',
    'goods_price_type': '货源类型,1:议价,2:一口价,默认:0全部',
})

request_order_list_param = api.doc(params={
    'goods_type': '货源类型,1:同城,2:跨城,3:零担,默认:0全部',
    'goods_price_type': '货源类型,1:议价,2:一口价,默认:0全部',
    'priority': '优先级,1:高,2:一般,3:默认:0全部',
    'vehicle_length': '车长要求,车长id,默认:0全部',
    'is_called': '是否通话：1:有,2:无,3:大于10次,默认：0全部',
    'is_addition': '是否加价,1:是,2:否,默认:0全部',
    'node_id': '所属网点:网点id,默认:0全部',
    'spec_tag': '特殊标签,1:初次下单,默认:0无',
    'mobile': '手机号',
    'page': '页数',
    'limit': '条数'
}, description='最新待接订单统计列表查询参数')


request_nearby_cars_param = api.doc(params={
    'goods_type': '车辆类型,1:接单线路,2:附近货车，默认:1:接单线路',
}, description='最新待接订单统计列表查询参数')