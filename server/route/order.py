# -*- coding: utf-8 -*-

from server import app
from server.meta.login_record import visitor_record
from server.meta.route_func import route_func
from server.route.all_route import all_route, all_route_html

order = all_route.order
order_html = all_route_html[order]


@app.route(order, endpoint='order')
@visitor_record
def order():
    """推广统计页面"""
    order = all_route.order
    return route_func(order, order_html)
