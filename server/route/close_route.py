#!/usr/bin/python
# -*- coding:utf-8 -*-
# author=hexm

from server import app
from server.meta.login_record import visitor_record
from server.meta.route_func import close_route_func


# 统一管理需要权限的路由
@app.route('/goods/', endpoint='goods')
@visitor_record
def goods_func():
    """货源统计页面"""
    return close_route_func('/goods/', '/goods/goods-statistics.html')


@app.route('/edit_sys_msg/', endpoint='edit_sys_msg')
@visitor_record
def edit_sys_msg_func():
    """消息中心修改页面"""
    return close_route_func('/edit_sys_msg/', '/edit_sys_msg/edit-sys-message.html')


@app.route('/distribution_map/', endpoint='distribution_map')
@visitor_record
def distribution_map():
    """分布图"""
    return close_route_func('/distribution_map/', '/map/distribution-map.html')


@app.route('/goods_map/', endpoint='goods_map')
@visitor_record
def goods_map():
    """货源热力地图"""
    return close_route_func('/goods_map/', '/map/goods-map.html')


@app.route('/users_map/', endpoint='users_map')
@visitor_record
def users_map():
    """用户热力地图"""
    return close_route_func('/users_map/', '/map/users-map.html')


@app.route('/edit-message/', endpoint='edit-message')
@visitor_record
def edit_message_func():
    """消息中心修改页面"""
    return close_route_func('/edit-message/', '/message/edit-message.html')


@app.route('/order/', endpoint='order')
@visitor_record
def order_func():
    """推广统计页面"""
    return close_route_func('/order/', '/order/order-statistics.html')


@app.route('/potential/', endpoint='potential')
@visitor_record
def potential_func():
    """潜在货源页面"""
    return close_route_func('/potential/', '/potential/potential-goods.html')


@app.route('/price/', endpoint='price')
@visitor_record
def price_func():
    """价格统计页面"""
    return close_route_func('/price/', '/price/price-statistics.html')


@app.route('/promote/', endpoint='promote')
@visitor_record
def promote_func():
    """推广统计页面"""
    return close_route_func('/promote/', '/promote/promote-statistics.html')


@app.route('/root/', endpoint='root_manage')
@visitor_record
def root_func():
    """用户管理页面"""
    return close_route_func('/root/', '/root/root.html')


@app.route('/transport/', endpoint='transport')
@visitor_record
def transport_func():
    """运力统计页面"""
    return close_route_func('/transport/', '/transport/transport-capacity.html')


@app.route('/user/', endpoint='user')
@visitor_record
def user_func():
    """用户统计页面"""
    return close_route_func('/user/', '/user/user-statistics.html')


@app.route('/active_retain/', endpoint='/active_retain/')
@visitor_record
def active_retain():
    """活跃留存页面"""
    return close_route_func('/active_retain/', '/user/active-retain.html')


@app.route('/vehicle/', endpoint='vehicle')
@visitor_record
def vehicle_func():
    """车辆认证页面"""
    return close_route_func('/vehicle/', '/vehicle/verify_vehicle.html')



