# -*- coding: utf-8 -*-

from flask import render_template, redirect

from server import app
from server.meta.session_operation import SessionOperationClass

avatar_url = "https://gss2.bdstatic.com/9fo3dSag_xI4khGkpoWK1HF6hhy/baike/c0%3Dbaike272%2C5%2C5%2C272%2C90/sign=e31d7a55dba20cf4529df68d17602053/91ef76c6a7efce1b27893518a451f3deb58f6546.jpg"


@app.route('/login/')
def login():
    """登录页面"""
    # 已登录返回首页
    if not SessionOperationClass.check():
        return render_template('/login/login.html')
    return redirect('/home/')


@app.route('/', endpoint='index')
@app.route('/index/', endpoint='index')
def home_func():
    """主页"""
    version = "1.0.0"
    return render_template('/admin/home.html/', user_name="游客", avatar_url=avatar_url, locations="", version=version)



