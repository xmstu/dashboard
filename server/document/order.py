from flask_restplus import fields
from server.status import APIStatus, FeedAPIStatus
from server import api

response_success = api.response(200, '成功', api.model('response_success', {
    'state': fields.Integer(description=str(APIStatus.Ok)),
    'msg': fields.String(description=FeedAPIStatus.Decriptions[APIStatus.Ok]),
}))

request_order_received_statistics_param = api.doc(params={
    'start_time': '开始时间',
    'end_time': '结束时间',
    'periods': '按日，按周，按月',
    'goods_type': '货源类型',
    'dimension': '维度',
    'region_id': '地区id',
    'comment_type': '评价',
    'pay_method': '支付方式'
}, description='订单统计请求参数')


request_cancel_order_reason_param = api.doc(params={
    'start_time': '开始时间',
    'end_time': '结束时间',
    'goods_type': '货源类型',
    'cancel_type': '取消原因:1.司机取消;2.货主取消',
    'region_id': '地区id'
}, description='取消订单原因请求参数')


request_order_list_param = api.doc(params={
    'order_id': '订单ID',
    'consignor_mobile': '货主手机',
    'driver_mobile': '司机手机',
    'from': '出发地',
    'to': ' 目的地',
    'order_status': '订单状态',
    'order_type': '订单类型',
    'vehicle_length': '车长要求',
    'vehicle_type': '车型要求',
    'node_id': '所属网点',
    'spec_tag': '特殊标签',
    'pay_status': '支付状态',
    'is_change_price': '是否改价',
    'comment_type': '评价',
    'start_order_time': '开始接单时间',
    'end_order_time': '结束接单时间',
    'start_loading_time': '开始装货时间',
    'end_loading_time': '结束装货时间'
}, description='订单列表请求参数')

