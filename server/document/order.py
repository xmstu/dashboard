from flask_restplus import fields
from server.status import APIStatus, FeedAPIStatus
from server import api

response_success = api.response(200, '成功', api.model('response_success', {
    'state': fields.Integer(description=str(APIStatus.Ok)),
    'msg': fields.String(description=FeedAPIStatus.Decriptions[APIStatus.Ok]),
}))

request_order_received_statistics_param = api.doc(params={
    'start_time': '开始日期(时间戳),默认:8天前',
    'end_time': '结束日期(时间戳),默认:昨天',
    'periods': '时间周期,2:日，3:周，4:月，默认:2',
    'goods_type': '货源类型,1:跨城,2:同城,默认:0全部',
    'goods_price_type': '货源类型,1:议价,2:一口价,默认:0全部',
    'dimension': '维度,1:按数量,2：按金额,默认:1',
    'region_id': '地区id,默认:0全部',
    'comment_type': '评价:1:好评,2:中评,3:差评,默认:0全部',
    'pay_method': '支付方式,1:未支付,2:线上支付,3:线下支付,默认:0全部'
}, description='订单统计请求参数')


request_cancel_order_reason_param = api.doc(params={
    'start_time': '开始时间',
    'end_time': '结束时间',
    'goods_type': '货源类型',
    'goods_price_type': '货源类型,1:议价,2:一口价,默认:0全部',
    'cancel_type': '取消原因:1.司机取消;2.货主取消',
    'region_id': '地区id'
}, description='取消订单原因请求参数')


request_order_list_param = api.doc(params={
    'order_id': '订单ID',
    'consignor_mobile': '货主手机',
    'driver_mobile': '司机手机',
    'from_province_id': '出发地省份',
    'from_city_id': '出发地城市',
    'from_county_id': '出发地区镇',
    'to_province_id': ' 目的地省份',
    'to_city_id': ' 目的地城市',
    'to_county_id': ' 目的地区镇',
    'order_status': '订单状态',
    'order_type': '订单距离类型',
    'order_price_type': '订单价格类型',
    'vehicle_length': '车长要求',
    'vehicle_type': '车型要求',
    'node_id': '所属网点',
    'spec_tag': '特殊标签',
    'pay_status': '支付状态',
    'is_change_price': '是否改价',
    'comment_type': '评价',
    'start_order_time': '开始接单时间',
    'end_order_time': '结束接单时间',
    'start_complete_time': '开始完成时间',
    'end_complete_time': '结束完成时间',
    'register_start_time': '货主注册开始时间',
    'register_end_time': '货主注册结束时间',
    'page': '页数',
    'limit': '条数'
}, description='订单列表请求参数')

