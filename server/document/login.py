#!/usr/bin/python
# -*- coding:utf-8 -*-

# Copyright (c) 2016 yu.liu <showmove@qq.com>
# All rights reserved

from flask_restplus import reqparse, fields

from server.status import UserAPIStatus
from server import api

payload = {"mobile": fields.Integer(description='手机号码'),
           'password': fields.String(description="密码")
           }

captchlogin = {
    "mobile": fields.Integer(description='未注册人的手机号码'),
    "password": fields.String(description="密码"),
    "code": fields.Integer(description="验证码"),
    'user_name': fields.String(description='用户名'),
    'avatar_url': fields.String(description='头像url地址'),
    'user_type': fields.Float(description='用户类型：1货主，2车主，3物流公司')
}

info_data_model = api.model(name='user_login', model={
    "raw_data": fields.String(description='原始数据字符串', required=True),
    "signature": fields.String(description='签名字符串', required=True),
    "encrypted_data": fields.String(description='加密数据', required=True),
    "iv": fields.String(description='加密算法的初始向量', required=True)
})

miniprogram_login = {
    "mobile": fields.String(description='手机号码', required=True),
    "code": fields.String(description="验证码", required=True),
    'app_id': fields.String(description='省省回头车appid', required=True),
    'user_info_data': fields.Nested(info_data_model, description='用户信息的加密数据', required=True),
    'share_info_data': fields.Nested(info_data_model, description='分享信息的加密数据')
}

mini_program_register_with_code = {
    "mobile": fields.String(description='手机号码', required=True),
    "code": fields.String(description="微信", required=True),
    "captcha_code": fields.String(description="验证码", required=True),
}
api_user_mini_program_register_with_code_doc = api.doc(body=api.model(name="mini_program_register_with_code",
                                                                      model=mini_program_register_with_code),
                                                       description="小程序注册通过code")

mini_program_login = {
    "code": fields.String(description="微信", required=True)
}
api_user_mini_program_login_doc = api.doc(body=api.model(name="mini_program_login",
                                                         model=mini_program_login),
                                          description="小程序一键登录")

h5_login = {
    "mobile": fields.String(description='手机号码', required=True),
    "code": fields.String(description="验证码", required=True),
}

user_register_model = api.model(name='user_login', model=payload)
user_login_captch_model = api.model(name="user_login_captch", model=captchlogin)

api_user_register_doc = api.doc(body=user_register_model, description="用户登录")
api_user_login_captch_doc = api.doc(body=user_login_captch_model, description="短信登录")

api_user_miniprogram_login_captch_doc = api.doc(body=api.model(name="miniprogram_login", model=miniprogram_login),
                                                description="小程序验证码登录")
api_user_h5_login_captch_doc = api.doc(body=api.model(name="H5_login", model=h5_login), description="H5验证码登录")

api_user_miniprogram_header = api.header('sessionId', type=str, description="会话ID")

response_user_login_success = api.response(200, '成功',
                                           api.model('xx_user_login_success', {
                                               'status': fields.Integer(description=str(UserAPIStatus.Ok)),
                                               'msg': fields.String(
                                                   description=UserAPIStatus.Decriptions[UserAPIStatus.Ok]),
                                               'data_xx': fields.Nested(
                                                   api.model('tokens', {'token': fields.String(description="用户TOKEN"),
                                                                        'refresh_token': fields.String(
                                                                            description="refresh_token"),
                                                                        'im': fields.Nested(api.model("im_response", {
                                                                            "username": fields.String(
                                                                                description="用户名"),
                                                                            "password": fields.String(
                                                                                description="密码")}))}))}))

response_user_miniprogram_login_success = api.response(200, '成功',
                                                       api.model('x_user_login_success', {
                                                           'status': fields.Integer(description=str(UserAPIStatus.Ok)),
                                                           'msg': fields.String(
                                                               description=UserAPIStatus.Decriptions[UserAPIStatus.Ok]),
                                                           'data': fields.Nested(api.model('tokens', {
                                                               'token': fields.String(description="用户TOKEN")})),
                                                       }))

refresh_payload = {'refresh_token': fields.String(description="密码")}
user_refresh_model = api.model(name='user_refresh', model=refresh_payload)
api_user_refresh_doc = api.doc(body=user_refresh_model, description="用户刷新")
response_user_refresh_success = api.response(200, '成功',
                                             api.model('user_refresh_success', {
                                                 'status': fields.Integer(description=str(UserAPIStatus.Ok)),
                                                 'msg': fields.String(
                                                     description=UserAPIStatus.Decriptions[UserAPIStatus.Ok]),
                                                 'data': fields.Nested(api.model('tokens', {
                                                     'token': fields.String(description="用户TOKEN"),
                                                     'refresh_token': fields.String(description="refresh_token")}
                                                                                 ))
                                             }))
