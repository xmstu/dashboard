# -*- coding: utf-8 -*-

from server import app
from server.meta.login_record import visitor_record
from server.meta.route_func import route_func
from server.route.all_route import all_route, all_route_html

user = all_route.user
user_html = all_route_html[user]


@app.route(user, endpoint='user')
@visitor_record
def user():
    """用户统计页面"""
    return route_func(user, user_html)
