# -*- coding: utf-8 -*-

from server import app
from flask import render_template

@app.route('/login/')
def login():
    """登录页面"""
    return render_template('/login/login.html')