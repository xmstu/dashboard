# -*- coding: utf-8 -*-

from server import app
from server.meta.login_record import visitor_record
from server.meta.route_func import route_func
from server.route.all_route import all_route, all_route_html

potential = all_route.potential
potential_html = all_route_html[potential]


@app.route(potential, endpoint='potential')
@visitor_record
def potential():
    """潜在货源页面"""
    return route_func(potential, potential_html)
