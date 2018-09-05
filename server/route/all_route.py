#!/usr/bin/python
# -*- coding:utf-8 -*-
# author=hexm
from server.meta.creators import DictModel


all_route = DictModel({
    'edit_sys_msg': '/edit_sys_msg/',
    'goods': '/goods/',
    'home': '/home/',
    'map': '/map/',
    'message': '/message/',
    'edit_message': '/edit-message/',
    'order': '/order/',
    'potential': '/potential/',
    'price': '/price/',
    'promote': '/promote/',
    'root': '/root/',
    'transport': '/transport/',
    'user': '/user/',
    'vehicle': '/vehicle/',
})

all_route_html = {
    '/edit_sys_msg/': '/edit_sys_msg/edit-sys-message.html',
    '/goods/': '/goods/goods-statistics.html',
    '/home/': '/admin/home.html',
    '/map/': '/map/heat-map.html',
    '/message/': '/message/message.html',
    '/edit-message/': '/message/edit-message.html',
    '/order/': '/order/order-statistics.html',
    '/potential/': '/potential/potential-goods.html',
    '/price/': '/price/price-statistics.html',
    '/promote/': '/promote/promote-statistics.html',
    '/root/': '/root/root.html',
    '/transport/': '/transport/transport-capacity.html',
    '/user/': '/user/user-statistics.html',
    '/vehicle/': '/vehicle/verify_vehicle.html',
}
