# -*- coding: utf-8 -*-

from server import app
from flask import render_template, session

@app.route('/promote/')
def promote():
    """推广统计页面"""
    if not session.get('login'):
        return render_template('/login/login.html')
    return render_template('/promote/promote-statistics.html')