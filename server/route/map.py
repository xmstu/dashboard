# -*- coding: utf-8 -*-

from server import app
from server.meta.login_record import visitor_record
from server.meta.route_func import route_func
from server.route.all_route import all_route, all_route_html

map = all_route.map
map_html = all_route_html[map]


@app.route(map, endpoint='map')
@visitor_record
def map():
    """热力图"""
    return route_func(map, map_html)
