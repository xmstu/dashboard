# -*- coding: utf-8 -*-

from server import app
from server.meta.login_record import visitor_record
from server.meta.route_func import route_func
from server.route.all_route import all_route, all_route_html

price = all_route.price
price_html = all_route_html[price]


@app.route(price, endpoint='price')
@visitor_record
def price():
    """价格统计页面"""
    price = all_route.price
    return route_func(price, price_html)
