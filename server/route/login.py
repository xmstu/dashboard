# -*- coding: utf-8 -*-

from flask import render_template, redirect, request

from server import app
from server.cache_data import init_regions
from server.database import db
from server.logger import log
from server.meta.session_operation import sessionOperationClass
from server.models.login import Login
from server.utils.broker_token import decode
from server.utils.init_regions import InitRegionModel


@app.route('/login/')
def login():
    """登录页面"""
    # 已登录返回首页
    if sessionOperationClass.check():
        return redirect('/home/')
    return render_template('/login/login.html')


@app.route('/broker/')
def broker():
    """区镇合伙人登录"""
    try:
        # 清空登录信息
        if sessionOperationClass.check():
            sessionOperationClass.deleted()
        # 区镇合伙人验证
        token = request.args.get('token', None)
        if not token:
            log.warn('区镇合伙人token传值错误')
            return render_template('/exception/except.html', status_coder=400, title='参数错误',
                                   content='区镇合伙人token传值错误')
        # token解码
        payload = decode(token)
        mobile = payload.get('mobile')
        if not mobile:
            log.warn('区镇合伙人无法获取mobile: [token: %s]' % token)
            return render_template('/exception/except.html', status_coder=400, title='参数错误',
                                   content='区镇合伙人无法获取电话')
        # 查询用户区域
        result = Login.get_partner_user(db.read_db, mobile)
        if not result:
            log.warn('区镇合伙人查询区域为空: [mobile: %s]' % mobile)
            return render_template('/exception/except.html', status_coder=400, title='参数错误',
                                   content='区镇合伙人查询区域为空')
        user_info = {
            'id': result[0]['user_id'],
            'user_name': result[0]['user_name'],
            'mobile': result[0]['mobile'],
            'avatar_url': result[0]['avatar_url'],
            'account': result[0]['mobile']
        }
        role = result[0]['role']
        locations = [location['region_id'] for location in result]
        locations = set(locations)
        # 先将locations中所有region_id的父级id查出来，然后去重
        parent_id_set = {init_regions.get_parent_id(i) for i in locations}
        # 再求出每个父id的子id集合，看该子id集合是否为location的子集，是的话，就将该父id加进location
        for parent_id in parent_id_set:
            child_id_set = InitRegionModel.get_child_id(db.read_db, parent_id)
            if child_id_set <= locations:
                locations.add(parent_id)

        # 登录
        if sessionOperationClass.insert(user_info, role, locations):
            return redirect('/home/')
        else:
            return render_template('/exception/except.html', status_coder=400, title='参数错误',
                                   content='登录写入session失败')
    except Exception as e:
        log.error('区镇合伙人登录异常: [error: %s]' % e, exc_info=True)
