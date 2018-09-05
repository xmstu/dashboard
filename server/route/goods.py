# -*- coding: utf-8 -*-

from server import app
from server.meta.login_record import visitor_record
from server.meta.route_func import route_func
from server.route.all_route import all_route, all_route_html

goods = all_route.goods
goods_html = all_route_html[goods]


@app.route(goods, endpoint='goods')
@visitor_record
def goods():
    """货源统计页面"""
    return route_func(goods, goods_html)
