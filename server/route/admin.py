# -*- coding: utf-8 -*-
from server import app
from flask import render_template, session, redirect

@app.route('/home/')
def home():
    """货源统计页面"""
    if not session.get('login'):
        return redirect('/login/')
    # 用户名，头像, 地区
    user_name = session['login'].get('user_name', '')
    avatar_url = session['login'].get('avatar_url', 'https://mp.huitouche.com/static/images/newicon.png')
    locations = session['login'].get('locations', [])
    return render_template('/admin/home.html', user_name=user_name, avatar_url=avatar_url, locations=locations)