import json

from server.cache_data import init_regions
from server.meta.decorators import make_decorator
from server.status import make_result, APIStatus, HTTPStatus
from server.utils.constant import d_user, d_goods, d_vehicle, d_order
from server.utils.extend import ExtendHandler


class DistributionMap(object):

    @staticmethod
    @make_decorator
    def get_result(params, data):

        dimension = {
            1: d_user.get(params['field']),
            2: d_goods.get(params['field']),
            3: d_vehicle.get(params['field']),
            4: d_order.get(params['field'])
        }

        if params['dimension']:
            ret_list = data['ret_list']
            region_group = data['region_group']
            if ret_list:
                for detail in ret_list:
                    name = init_regions.to_region(detail[region_group])
                    if '省' in name:
                        name = name[:-1]
                    detail['name'] = name

                all_data = json.loads(json.dumps(ret_list, default=ExtendHandler.handler_to_float))
                all_data = sorted(all_data, key=lambda i: -i['count'])
                max_value, min_value = all_data[0]['count'], all_data[-1]['count'] if len(all_data) > 0 else (0, 0)

                value = dimension.get(params['dimension'])
                # 构造map_data
                map_data = []
                toolTipData = []
                sum_value = 0
                for i in all_data:
                    sum_value += i.get('count', 0)
                    map_data.append({
                        'name': i.get('name', ''),
                        'value': i.get('count', 0)
                    })
                    toolTipData.append({
                        "name": i.get('name', ''),
                        "value": [{
                            "name": value,
                            "value": i.get('count', 0)
                        }]
                    })
            else:
                all_data, map_data, toolTipData = [], [], []
                max_value, min_value, sum_value = (0, 0, 0)
        else:
            all_data, map_data, toolTipData = [], [], []
            max_value, min_value, sum_value = (0, 0, 0)

        data = {
            "all_data ": all_data,
            "map_data": map_data,
            "toolTipData": toolTipData,
            "max_value": max_value,
            "min_value": min_value,
            "sum_value": sum_value,
            "authority_region_id": params.get('authority_region_id', 0)
        }

        return make_result(APIStatus.Ok, data=data), HTTPStatus.Ok


class GoodsMap(object):

    @staticmethod
    @make_decorator
    def get_result(data):
        # TODO 过滤参数

        return make_result(APIStatus.Ok), HTTPStatus.Ok


class UsersMap(object):

    @staticmethod
    @make_decorator
    def get_result(data):
        # TODO 过滤参数

        return make_result(APIStatus.Ok), HTTPStatus.Ok