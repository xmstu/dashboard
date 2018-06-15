# -*- coding: utf-8 -*-

from server import app
from flask import render_template, session, redirect

@app.route('/login/')
def login():
    """登录页面"""
    # 已登录返回首页
    if session.get('login'):
        return redirect('/home/')
    return render_template('/login/login.html')