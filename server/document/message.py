# -*- coding: utf-8 -*-

from server import api
from flask_restplus import fields

request_system_message_list_get = api.doc(params={
    'page': '页数',
    'limit': '条数',
})

request_system_message_post = api.doc(body=api.model('request_system_message_post', {
    'title': fields.String(description='消息标题'),
    'content': fields.String(description='消息内容'),
    'msg_type': fields.Integer(description='消息类型: 1.手动发布, 2自动发布'),
    'push_role': fields.Integer(description='推送角色: 0.全部,1.后台用户,2.区镇合伙人,3.网点管理员,4.城市经理')
}))

request_system_message_put = api.doc(body=api.model('request_system_message_put', {
    'title': fields.String(description='消息标题'),
    'content': fields.String(description='消息内容'),
    'msg_type': fields.Integer(description='消息类型: 1.手动发布, 2自动发布'),
    'push_role': fields.Integer(description='推送角色: 0.全部,1.后台用户,2.区镇合伙人,3.网点管理员,4.城市经理')
}))

request_user_message_list_get = api.doc(params={
    'user_name': '用户名',
    'page': '页数',
    'limit': '条数',
})

request_user_message_read_put = api.doc(body=api.model('request_user_message_read_post', {
    'user_name': fields.String(description='用户名'),

}))

response_system_message_list_get = api.response(200, '成功', api.model('response_system_message_list_get', {
    'state': fields.Integer(description='100000'),
    'msg': fields.String(description='成功'),
    'count': fields.Integer(description='总消息数'),
    'data': fields.Nested(model=api.model('goods_id', {
        'id': fields.Integer(description='消息id'),
        'title': fields.String(description='消息标题'),
        'content': fields.String(description='消息内容'),
        'user_id': fields.Integer(description='发布者id'),
        'create_time': fields.String(description='消息发布时间'),
        'update_time': fields.String(description='消息修改时间'),
        'msg_type': fields.Integer(description='消息类型: 1.手动发布, 2自动发布'),
        'is_deleted': fields.Integer(description='是否删除')
    }), description='货物ID')
}))

response_user_message_list_get = api.response(200, '成功', api.model('response_user_message_list_get', {
    'state': fields.Integer(description='100000'),
    'msg': fields.String(description='成功'),
    'unread': fields.Integer(description='未读消息数'),
    'count': fields.Integer(description='总消息数'),
    'data': fields.Nested(model=api.model('goods_id', {
        'is_read': fields.Integer(description='是否已读,0未读,1已读'),
        'id': fields.Integer(description='消息id'),
        'title': fields.String(description='消息标题'),
        'content': fields.String(description='消息内容'),
        'create_time': fields.String(description='消息发布时间')
    }), description='货物ID')
}))