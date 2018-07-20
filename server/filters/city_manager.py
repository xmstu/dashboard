# -*- coding: utf-8 -*-

from server.meta.decorators import make_decorator
from server.status import make_result, APIStatus, HTTPStatus

class cityManagerFilter(object):
    @staticmethod
    @make_decorator
    def filter_data(data):
        auth_driver = 0
        goods_count = 0
        order_count = 0
        for i in data:
            if i.get('auth_driver'):
                auth_driver += 1
            if i.get('goods_count'):
                goods_count += i['goods_count']
            if i.get('order_count'):
                order_count += i['order_count']

        result = {
            'auth_driver': auth_driver,
            'goods_count': goods_count,
            'order_count': order_count
        }

        return make_result(APIStatus.Ok, data=result), HTTPStatus.Ok