from flask_restplus import fields

from server import api
from server.status import APIStatus, FeedAPIStatus

request_order_list_param = api.doc(params={
    'goods_type': '货源类型',
    'priority': '优先级',
    'vehicle_length': '车长要求',
    'is_called': '是否通话',
    'is_addition': '是否加价',
    'node_id': '所属网点',
    'new_goods_type': '初次下单',
    'page': '页数',
    'limit': '条数'
}, description='最新待接订单统计列表查询参数')

response_order_list_param_success = api.response(200, '成功', api.model('response_success', {
    'state': fields.Integer(description=str(APIStatus.Ok)),
    'msg': fields.String(description=FeedAPIStatus.Decriptions[APIStatus.Ok]),
}))
