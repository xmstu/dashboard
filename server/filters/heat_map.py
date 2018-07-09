import json

from server.cache_data import init_regions
from server.meta.decorators import make_decorator
from server.status import make_result, APIStatus, HTTPStatus
from server.utils.extend import ExtendHandler


class HeatMap(object):

    @staticmethod
    @make_decorator
    def get_result(params, data):
        # TODO 过滤参数
        if params['dimension'] == 1:
            pass

        elif params['dimension'] == 2:
            goods_list = data['goods_list']
            region_group = data['region_group'].split('.')[1]
            for detail in goods_list:
                detail['name'] = init_regions.to_region(detail[region_group])

            map_data = json.loads(json.dumps(goods_list, default=ExtendHandler.handler_to_float))
            # 根据点击的字段排序,获取最大最小值
            if params['field'] == 1:
                map_data = sorted(map_data, key=lambda i: i['goods_count'])
                max_value, min_value = map_data[-1]['goods_count'], map_data[0]['goods_count']
            elif params['field'] == 2:
                map_data = sorted(map_data, key=lambda i: i['goods_price'])
                max_value, min_value = map_data[-1]['goods_price'], map_data[0]['goods_price']
            elif params['field'] == 3:
                map_data = sorted(map_data, key=lambda i: i['orders_count'])
                max_value, min_value = map_data[-1]['orders_count'], map_data[0]['orders_count']
            elif params['field'] == 4:
                map_data = sorted(map_data, key=lambda i: i['orders_price'])
                max_value, min_value = map_data[-1]['orders_price'], map_data[0]['orders_price']

        elif params['dimension'] == 3:
            pass

        else:
            map_data = [{}]

        return make_result(APIStatus.Ok, data={"map_data ": map_data, "max_value": max_value, "min_value": min_value}), HTTPStatus.Ok
