# -*- coding: utf-8 -*-

from server import app
from server.meta.login_record import visitor_record
from server.meta.route_func import route_func
from server.route.all_route import all_route, all_route_html

edit_sys_msg = all_route.edit_sys_msg
edit_sys_msg_html = all_route_html[edit_sys_msg]


@app.route(edit_sys_msg, endpoint='edit_sys_msg')
@visitor_record
def edit_sys_msg():
    """消息中心修改页面"""
    edit_sys_msg = all_route.edit_sys_msg
    return route_func(edit_sys_msg, edit_sys_msg_html)
