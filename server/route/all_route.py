#!/usr/bin/python
# -*- coding:utf-8 -*-
# author=hexm

from server import app
from server.meta.login_record import visitor_record
from server.meta.route_func import route_func


# RouteUrl = namedtuple('RouteUrl', ['route', 'endpoint', 'template'])


@app.route('/goods/', endpoint='goods')
@visitor_record
def goods_func():
    """货源统计页面"""
    return route_func('/goods/', '/goods/goods-statistics.html')


@app.route('/edit_sys_msg/', endpoint='edit_sys_msg')
@visitor_record
def edit_sys_msg_func():
    """消息中心修改页面"""
    return route_func('/edit_sys_msg/', '/edit_sys_msg/edit-sys-message.html')


@app.route('/admin/', endpoint='admin')
@visitor_record
def home_func():
    """主页"""
    return route_func('/admin/', '/admin/home.html/')


@app.route('/map/', endpoint='map')
@visitor_record
def map_func():
    """热力图"""
    return route_func('/map/', '/map/heat-map.html')


@app.route('/message/', endpoint='message')
@visitor_record
def message_func():
    """消息列表"""
    return route_func('/message/', '/message/message.html')


@app.route('/edit-message/', endpoint='edit-message')
@visitor_record
def edit_message_func():
    """消息中心修改页面"""
    return route_func('/edit-message/', '/message/edit-message.html')


@app.route('/order/', endpoint='order')
@visitor_record
def order_func():
    """推广统计页面"""
    return route_func('/order/', '/order/order-statistics.html')


@app.route('/potential/', endpoint='potential')
@visitor_record
def potential_func():
    """潜在货源页面"""
    return route_func('/potential/', '/potential/potential-goods.html')


@app.route('/price/', endpoint='price')
@visitor_record
def price_func():
    """价格统计页面"""
    return route_func('/price/', '/price/price-statistics.html')


@app.route('/promote/', endpoint='promote')
@visitor_record
def promote_func():
    """推广统计页面"""
    return route_func('/promote/', '/promote/promote-statistics.html')


@app.route('/root/', endpoint='root_manage')
@visitor_record
def root_func():
    """用户管理页面"""
    return route_func('/root/', '/root/root.html')


@app.route('/transport/', endpoint='transport')
@visitor_record
def transport_func():
    """运力统计页面"""
    return route_func('/transport/', '/transport/transport-capacity.html')


@app.route('/user/', endpoint='user')
@visitor_record
def user_func():
    """用户统计页面"""
    return route_func('/user/', '/user/user-statistics.html')


@app.route('/vehicle/', endpoint='vehicle')
@visitor_record
def vehicle_func():
    """车辆认证页面"""
    return route_func('/vehicle/', '/vehicle/verify_vehicle.html')
