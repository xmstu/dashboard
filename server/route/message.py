# -*- coding: utf-8 -*-

from server import app
from server.meta.login_record import visitor_record
from server.meta.route_func import route_func
from server.route.all_route import all_route, all_route_html

message = all_route.message
edit_message = all_route.edit_message
message_html = all_route_html[message]
edit_message_html = all_route_html[edit_message]


@app.route(message, endpoint='message')
@visitor_record
def message():
    """消息列表"""
    return route_func(message, message_html)


@app.route(edit_message, endpoint='edit_message')
@visitor_record
def edit_message():
    """消息中心修改页面"""
    return route_func(edit_message, edit_message_html)
