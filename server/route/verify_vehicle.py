# -*- coding: utf-8 -*-

from server import app
from server.meta.login_record import visitor_record
from server.meta.route_func import route_func
from server.route.all_route import all_route, all_route_html

vehicle = all_route.vehicle
vehicle_html = all_route_html[vehicle]


@app.route(vehicle, endpoint='vehicle')
@visitor_record
def vehicle():
    """车辆认证页面"""
    return route_func(vehicle, vehicle_html)
