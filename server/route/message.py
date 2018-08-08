# -*- coding: utf-8 -*-
import re
from threading import Lock

from flask import render_template, session, redirect

from server import app, socketio
from server.cache_data import init_regions
from server.database import db
from server.meta.login_record import visitor_record
from server.meta.session_operation import sessionOperationClass
from server.models.long_term_vehicle import LongTermVehiclModel
from server.models.message import MessageSystemModel

thread = None
thread_lock = Lock()


@app.route('/message/', endpoint='message')
@visitor_record
def message():
    """消息列表"""
    if not sessionOperationClass.check():
        return redirect('/login/')
    # 用户名，头像, 地区
    user_name = session['login'].get('user_name', '')
    account = session['login'].get('account', '')
    avatar_url = session['login'].get('avatar_url', 'https://mp.huitouche.com/static/images/newicon.png')
    locations = [{'region_id': i, 'name': init_regions.to_full_short_name(i)} for i in
                 session['login'].get('locations', [])]
    role = session['login'].get('role', 0)
    if role == 4:
        locations = init_regions.get_city_next_region(session['login'].get('locations', []))
    return render_template('/message/message.html', user_name=user_name, avatar_url=avatar_url, locations=locations,
                           role=role, account=account, async_mode=socketio.async_mode)


@app.route('/edit-message/', endpoint='edit-message')
@visitor_record
def message():
    """消息管理"""
    if not sessionOperationClass.check():
        return redirect('/login/')
    # 用户名，头像, 地区
    user_name = session['login'].get('user_name', '')
    account = session['login'].get('account', '')
    avatar_url = session['login'].get('avatar_url', 'https://mp.huitouche.com/static/images/newicon.png')
    locations = [{'region_id': i, 'name': init_regions.to_full_short_name(i)} for i in
                 session['login'].get('locations', [])]
    role = session['login'].get('role', 0)
    if role == 4:
        locations = init_regions.get_city_next_region(session['login'].get('locations', []))
    return render_template('/message/edit-message.html', user_name=user_name, avatar_url=avatar_url,
                           locations=locations, role=role, account=account)


# 后台线程 产生数据，即刻推送至前端
def background_thread():
    """Example of how to send server generated events to clients."""
    new_count = 0
    last_count = 0
    while True:
        now_count = LongTermVehiclModel.get_count(db.read_db)
        if now_count and last_count:
            new_count = now_count - last_count
        new_data = LongTermVehiclModel.get_data(db.read_db, new_count)
        if new_count and new_data:
            # 将新添加的长期用车信息写进系统信息表
            params_list = handle(new_data)
            for params in params_list:
                MessageSystemModel.insert_system_message(db.read_db, params)
            # 将数据发送给对应地区的区镇合伙人，实际上是写数据到对应的user_id

            socketio.emit('server_response', {'data': '你有新的消息！'}, namespace='/auto_message')
        last_count = now_count
        # 下次更新推送消息时隔10分钟
        socketio.sleep(600)


@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)


def handle(data):
    title = '长期用车'
    user_id = 322
    msg_type = 2
    for detail in data:
        detail.setdefault('title', title)
        detail.setdefault('user_id', user_id)
        detail.setdefault('msg_type', msg_type)

        content = detail.get('content', '')
        load_address = re.search('装货-地址：(.*?)<br>', content).group(1)
        print(load_address)

        unload_address = re.search('卸货-地址：(.*?)<br>', content).group(1)
        print(unload_address)

        long_lat = re.findall('(\d+\.\d+)', content)
        print(long_lat)

    return data
