# -*- coding: utf-8 -*-

from server import app
from server.meta.login_record import visitor_record
from server.meta.route_func import route_func
from server.route.all_route import all_route, all_route_html

promote = all_route.promote
promote_html = all_route_html[promote]


@app.route(promote, endpoint='promote')
@visitor_record
def promote():
    """推广统计页面"""
    promote = all_route.promote
    return route_func(promote, promote_html)
