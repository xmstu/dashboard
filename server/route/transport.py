# -*- coding: utf-8 -*-

from server import app
from server.meta.login_record import visitor_record
from server.meta.route_func import route_func
from server.route.all_route import all_route, all_route_html

transport = all_route.transport
transport_html = all_route_html[transport]


@app.route(transport, endpoint='transport')
@visitor_record
def transport():
    """运力统计页面"""
    transport = all_route.transport
    return route_func(transport, transport_html)
