# -*- coding: utf-8 -*-

from server import app
from flask import render_template, session

@app.route('/user/')
def user():
    """用户统计页面"""
    if not session.get('login'):
        return render_template('/login/login.html')
    return render_template('/user/user-statistics.html')