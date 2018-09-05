# -*- coding: utf-8 -*-

from server import app
from server.meta.login_record import visitor_record
from server.meta.route_func import route_func
from server.route.all_route import all_route, all_route_html

root = all_route.root
root_html = all_route_html[root]


@app.route('/root/', endpoint='root_manage')
@visitor_record
def root():
    """用户管理页面"""
    return route_func(root, root_html)
