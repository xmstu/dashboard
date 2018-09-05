# -*- coding: utf-8 -*-
from server import app
from server.meta.login_record import visitor_record
from server.meta.route_func import route_func
from server.route.all_route import all_route, all_route_html

home = all_route.home
home_html = all_route_html[home]


@app.route('/home/', endpoint='home')
@visitor_record
def home():
    """主页"""
    return route_func(home, home_html)
