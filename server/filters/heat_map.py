import json

from server.cache_data import init_regions
from server.meta.decorators import make_decorator
from server.status import make_result, APIStatus, HTTPStatus
from server.utils.constant import d_user, d_goods, d_name
from server.utils.extend import ExtendHandler


class HeatMap(object):

    @staticmethod
    @make_decorator
    def get_result(params, data):
        # TODO 过滤参数
        if params['dimension'] == 1:
            user_list = data['user_list']
            region_group = data['region_group']
            if user_list:
                for detail in user_list:
                    detail['name'] = init_regions.to_region(detail[region_group])
                all_data = json.loads(json.dumps(user_list, default=ExtendHandler.handler_to_float))
                all_data = sorted(all_data, key=lambda i: i['count'])
                max_value, min_value = all_data[-1]['count'], all_data[0]['count'] if len(all_data) > 0 else (0, 0)

                value = d_user.get(params['field'])
                # 构造map_data
                map_data = []
                toolTipData = []
                for i in all_data:
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
                max_value, min_value = (0, 0)

        elif params['dimension'] == 2:
            goods_list = data['goods_list']
            region_group = data['region_group'].split('.')[1]
            for detail in goods_list:
                detail['name'] = init_regions.to_region(detail[region_group])

            all_data = json.loads(json.dumps(goods_list, default=ExtendHandler.handler_to_float))
            # 根据点击的字段排序,获取最大最小值
            value = d_goods.get(params['field'])

            all_data = sorted(all_data, key=lambda i: i[value])
            max_value, min_value = all_data[-1][value], all_data[0][value] if len(all_data) > 0 else (0, 0)

            # 构造map_data
            map_data = []
            toolTipData = []
            for i in all_data:
                map_data.append({
                    'name': i.get('name', ''),
                    'value': i.get(value, 0)
                })
                toolTipData.append({
                    "name": i.get('name', ''),
                    "value": [{
                        "name": d_name.get(value, ''),
                        "value": i.get(value, 0)
                    }]
                })

        elif params['dimension'] == 3:
            pass

        else:
            all_data = [{}]

        data = {
            "all_data ": all_data,
            "map_data": map_data,
            "toolTipData": toolTipData,
            "max_value": max_value,
            "min_value": min_value
        }

        return make_result(APIStatus.Ok, data=data), HTTPStatus.Ok
