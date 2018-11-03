# -*- coding: utf-8 -*-

from flask import render_template, redirect

from server import app
from server.configs import avatar_url, version
from server.meta.session_operation import SessionOperationClass


@app.route('/login/')
def login():
    """登录页面"""
    # 已登录返回首页
    if not SessionOperationClass.check():
        return render_template('/login/login.html')
    return redirect('/home/')


@app.route('/index/', endpoint='index')
def index():
    """主页"""
    return render_template('/index/index.html/', user_name="游客", avatar_url=avatar_url, version=version)

@app.route('/goods/', endpoint='goods')
def goods():
    """主页"""
    return render_template('/goods/goods-statistics.html/', user_name="游客", avatar_url=avatar_url, version=version)