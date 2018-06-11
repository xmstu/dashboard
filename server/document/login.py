#!/usr/bin/python
# -*- coding:utf-8 -*-

# Copyright (c) 2016 yu.liu <showmove@qq.com>
# All rights reserved

from flask_restplus import fields
from server.status import APIStatus, FeedAPIStatus
from server import api

request_user_login = api.doc(body=api.model('request_user_login', {
    'user_name': fields.String(description='用户名'),
    'password': fields.String(description='密码')
    }, description='用户登录请求参数')
)

response_user_login_success = response_success = api.response(200, '成功', api.model('response_success', {
    'state': fields.Integer(description=str(APIStatus.Ok)),
    'msg': fields.String(description=FeedAPIStatus.Decriptions[APIStatus.Ok]),
}))
