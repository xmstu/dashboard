# -*- coding: utf-8 -*-

from server import api
from flask_restplus import fields


request_root_management_get = api.doc(params={
    'page': '页数',
    'limit': '条数',
})


request_root_management_add = api.doc(body=api.model('request_root_management_add', {
    'mobile': fields.String(description='手机号'),
    'comment': fields.String(description='用户备注'),
    'user_name': fields.String(description='用户名'),
    'password': fields.String(description='密码'),
    'role_id': fields.List(fields.Integer, description='角色id列表'),
}))

request_root_put = api.doc(body=api.model('request_root_put', {
    'mobile': fields.String(description='手机号'),
    'comment': fields.String(description='用户备注'),
    'user_name': fields.String(description='用户名'),
    'password': fields.String(description='密码'),
    'role_id': fields.List(fields.Integer, description='角色id列表'),
    'is_active': fields.Integer(description='是否启用:1.启用;2.禁用'),
}))

request_root_role_management_add = api.doc(body=api.model('request_root_role_management_add', {
    'type': fields.Integer(description='角色大类:管理员1,合伙人2,网点管理员3,城市经理4'),
    'role_name': fields.String(description='角色名称'),
    'role_comment': fields.String(description='角色备注'),
    'region_id': fields.Integer(description='地区id'),
    'page_id_list': fields.List(fields.Integer, description='页面id列表'),
}))


request_root_page_management_add = api.doc(body=api.model('request_root_page_management_add', {
    'page_name': fields.String(description='页面名称'),
    'page_comment': fields.String(description='页面备注'),
    'page_path': fields.String(description='页面路径'),
    'parent_menu_id': fields.Integer(description='页面的父菜单id'),
}))

request_root_menu_management_add = api.doc(body=api.model('request_root_menu_management_add', {
    'menu_name': fields.String(description='菜单名称'),
    'menu_comment': fields.String(description='菜单备注'),
    'page_id': fields.Integer(description='关联的页面id'),
    'parent_menu_id': fields.Integer(description='菜单的父菜单id'),
}))
