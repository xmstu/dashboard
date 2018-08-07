# -*- coding: utf-8 -*-
from server import api
from flask_restplus import fields


request_root_management_get = api.doc(params={
    'page': '页数',
    'limit': '条数',
})

request_root_management_delete = api.doc(params={
    'user_id': '用户id',
})

request_root_management_add = api.doc(body=api.model('request_root_management_add', {
    'account': fields.String(description='手机号'),
    'user_name': fields.String(description='用户名'),
    'password': fields.String(description='密码'),
    'region_id': fields.Integer(description='所属地id'),
}))

request_root_management_put = api.doc(body=api.model('request_root_management_put', {
    'account': fields.String(description='手机号'),
    'user_name': fields.String(description='用户名'),
    'password': fields.String(description='密码'),
    'region_id': fields.Integer(description='所属地id'),
}))

