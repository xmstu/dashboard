# -*- coding: utf-8 -*-

from server import app
from flask import render_template, session, redirect
from server.init_regions import init_regions

@app.route('/transport/')
def transport():
    """运力统计页面"""
    if not session.get('login'):
        return redirect('/login/')
    # 用户名，头像, 地区
    user_name = session['login'].get('user_name', '')
    avatar_url = session['login'].get('avatar_url', 'https://mp.huitouche.com/static/images/newicon.png')
    locations = [{'region_id': i, 'name': init_regions.to_full_short_name(i)} for i in
                 session['login'].get('locations', [])]
    return render_template('/transport/transport-capacity.html', user_name=user_name, avatar_url=avatar_url, locations=locations)