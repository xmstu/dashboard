# -*- coding: utf-8 -*-

from server import app
from server.logger import log
from flask import render_template, session, redirect, request
from flask import abort
from server.utils.broker_token import decode
from server.models.login import Login
from server.database import db
import time

@app.route('/login/')
def login():
    """登录页面"""
    # 已登录返回首页
    if session.get('login'):
        return redirect('/home/')
    return render_template('/login/login.html')

@app.route('/broker/')
def broker():
    """区镇合伙人登录"""
    if session.get('login'):
        return redirect('/home/')
    # 区镇合伙人验证
    token = request.args.get('token', None)
    if not token:
        log.warn('区镇合伙人token传值错误')
        abort(404)
    # token解码
    payload = decode(token)
    mobile = payload.get('mobile')
    if not mobile:
        log.warn('区镇合伙人无法获取mobile: [token: %s]' % token)
        abort(404)
    # 查询用户区域
    result = Login.get_partner_user(db.read_db, mobile)
    if not result:
        log.warn('区镇合伙人查询用户区域为空: [mobile: %s]' % mobile)
        abort(404)
    user_id = result[0]['user_id']
    user_name = result[0]['user_name']
    mobile = result[0]['mobile']
    avatar_url = result[0]['avatar_url']
    role = result[0]['role']
    locations = [location['region_id']for location in result]
    session['login'] = {
        'user_id': user_id,
        'user_name': user_name,
        'mobile': mobile,
        'avatar_url': avatar_url if avatar_url else 'https://mp.huitouche.com/static/images/newicon.png',
        'login_time': time.time(),
        'role': role,
        'locations': locations
    }
    return redirect('/home/')