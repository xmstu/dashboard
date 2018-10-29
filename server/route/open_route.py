# -*- coding: utf-8 -*-

from flask import render_template, redirect

from server import app
from server.meta.login_record import visitor_record
from server.meta.route_func import open_route_func
from server.meta.session_operation import SessionOperationClass


@app.route('/login/')
def login():
    """登录页面"""
    # 已登录返回首页
    if not SessionOperationClass.check():
        return render_template('/login/login.html')
    return redirect('/home/')


@app.route('/home/', endpoint='home')
@app.route('/admin/', endpoint='admin')
@visitor_record
def home_func():
    """主页"""
    return open_route_func('/admin/home.html/')


@app.route('/message/', endpoint='message')
@visitor_record
def message_func():
    """用户消息页面"""
    return open_route_func('/message/message.html')

