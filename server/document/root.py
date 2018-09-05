# -*- coding: utf-8 -*-
from server import api
from flask_restplus import fields


request_root_management_get = api.doc(params={
    'page': '页数',
    'limit': '条数',
})


request_root_management_add = api.doc(body=api.model('request_root_management_add', {
    'account': fields.String(description='手机号'),
    'user_name': fields.String(description='用户名'),
    'password': fields.String(description='密码'),
    'role_id': fields.Integer(description='角色id'),
}))

request_root_management_put = api.doc(body=api.model('request_root_management_put', {
    'account': fields.String(description='手机号'),
    'user_name': fields.String(description='用户名'),
    'password': fields.String(description='密码'),
    'role_id': fields.Integer(description='角色id'),
    'is_active': fields.Integer(description='是否启用:1.启用;2.禁用'),
}))

request_root_role_management_add = api.doc(body=api.model('request_root_role_management_add', {
    'role_name': fields.String(description='角色名称'),
    'role_comment': fields.String(description='角色备注'),
    'region_id': fields.Integer(description='地区id'),
    'page_id_list': fields.String(description='页面id列表'),
}))

request_root_role_management_put = api.doc(body=api.model('request_root_management_put', {
    'role_name': fields.String(description='角色名称'),
    'role_comment': fields.String(description='角色备注'),
    'region_id': fields.Integer(description='地区id'),
    'page_id_list': fields.String(description='页面id列表'),
}))
