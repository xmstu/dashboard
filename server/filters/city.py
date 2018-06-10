# -*- coding: utf-8 -*-

from server.meta.decorators import make_decorator
from server.status import build_result, HTTPStatus, APIStatus
from server.init_regions import init_regions
import json

import time

class CityResourceBalance(object):
    @staticmethod
    @make_decorator
    def get_result(goods, vehicle, params):
        # 货源车型
        result = {}
        for i in goods:
            if i['old_vehicle'] or i['new_vehicle']:
                vehicle_name = i['old_vehicle'] if i['old_vehicle'] else i['new_vehicle']
                result.setdefault(vehicle_name, {})
                if i['status'] == 1 or i['status'] == 2:
                    result[vehicle_name]['待接单'] = result[vehicle_name].setdefault('待接单', 0) + 1
                elif i['status'] == 3:
                    result[vehicle_name]['已接单'] = result[vehicle_name].setdefault('已接单', 0) + 1
                elif i['status'] == -1:
                    result[vehicle_name]['已取消'] = result[vehicle_name].setdefault('已取消', 0) + 1
                # 跨城议价
                if params['goods_type'] == 3:
                    if i['call_count'] == 0:
                        result[vehicle_name]['待联系'] = result[vehicle_name].setdefault('待联系', 0) + 1
                    else:
                        result[vehicle_name]['已联系'] =result[vehicle_name] .setdefault('已联系', 0) + 1
        # 接单车型
        for i in vehicle:
            if i['booking_vehicle']:
                result.setdefault(i['booking_vehicle'], {})
                if i['count']:
                    result[i['booking_vehicle']]['已接单车辆'] = result[i['booking_vehicle']].setdefault('已接单车辆', 0) + 1
                else:
                    result[i['booking_vehicle']]['待接单车辆数'] = result[i['booking_vehicle']].setdefault('待接单车辆数', 0) + 1
        # 合并结果
        city_result = {}
        for i in result:
            city_result[i] = [
                # 外圈
                [
                    {'value': result[i].get('待接单', 0), 'name': '待接单'},
                    {'value': result[i].get('已接单', 0), 'name': '已接单'},
                    {'value': result[i].get('已取消', 0), 'name': '已取消'}
                ],
                # 内圈
                [
                    {'value': result[i].get('已接单车辆', 0), 'name': '已接单车辆'},
                    {'value': result[i].get('待接单车辆数', 0), 'name': '待接单车辆数'},
                    {'value': 0, 'name': '空白部分', 'itemStyle': {
                        'normal': {
                            'color': 'rgba(0,0,0,0)',
                            'label': {'show': False},
                            'labelLine': {'show': False}},
                        'emphasis': {'color': 'rgba(0,0,0,0)'}}
                     }
                ]
            ]
            if params['goods_type'] == 3:
                city_result[i][0].extend([
                    {'value': result[i].get('待联系', 0), 'name': '待联系'},
                    {'value': result[i].get('已联系', 0), 'name': '已联系'}
                ])
        return build_result(APIStatus.Ok, data=city_result), HTTPStatus.Ok


class CityOrderListFilterDecorator(object):

    @staticmethod
    @make_decorator
    def get_result(data):
        goods = data['goods_detail']
        goods_counts = data['goods_counts']
        result = []
        for detail in goods:
            # 优先级
            if detail['goods_counts'] <= 3 or time.time() - detail['create_time'] <= 300 or detail['price_addition'] > 0:
                priority = '高'
            else:
                priority = '一般'
            # 货物类型
            if detail['type'] == 2:
                goods_type = '零担'
            elif detail['haul_dist'] == 1:
                goods_type = '同城'
            elif detail['haul_dist'] == 2 and detail['goods_level'] == 2:
                goods_type = '跨城定价'
            elif detail['haul_dist'] == 2 and detail['goods_level'] == 2:
                goods_type = '跨城议价'
            else:
                goods_type = ''
            # 货物规格
            name = detail.get('name', '')
            weight = str(int(detail['weight'] * 1000)) + '千克'\
                if detail.get('weight', 0) < 1 and detail.get('weight', 0) > 0\
                else str(int(detail.get('weight', 0))) + '吨'
            volume = str(int(detail.get('volume', 0))) + '平米'
            # 网点
            supplier_node = detail.get('supplier_node', '')
            # 出发地-目的地
            from_address = init_regions.to_address(detail.get('from_province_id', 0), detail.get('from_city_id', 0),
                                                  detail.get('from_county_id', 0)) + detail.get('from_address', '')
            to_address = init_regions.to_address(detail.get('to_province_id', 0), detail.get('to_city_id', 0),
                                                  detail.get('to_county_id', 0)) + detail.get('to_address', '')
            mileage_total = str(int(detail['mileage_total'] * 1000)) + '米'\
                if detail.get('mileage_total', 0) < 1 and detail.get('mileage_total', 0) > 0\
                else str(int(detail.get('mileage_total', 0))) + '千米'
            # 车长、车型
            if detail['new_vehicle_type'] and detail['new_vehicle_length']:
                vehicle = '\n'.join([detail['new_vehicle_type'], detail['new_vehicle_length']])
            else:
                vehicle = '\n'.join([detail.get('vehicle_type', ''), detail.get('vehicle_length', '')])
            # 发布、装货时间
            if detail['loading_time_period_begin']:
                loading_time = detail['shf_goods_loading_time_period_begin']
            else:
                if detail['loading_time_period'] == 1:
                    loading_time = detail.get('loading_time_date', '') + '08:00:00'
                elif detail['loading_time_period'] == 2:
                    loading_time = detail.get('loading_time_date', '') + '13:00:00'
                elif detail['loading_time_period'] == 3:
                    loading_time = detail.get('loading_time_date', '') + '19:00:00'
                else:
                    loading_time = detail.get('loading_time_date', '') + '00:00:00'
            goods_time = '发布时间:%(create_time)s\n装货时间%(loading_time)s' % {
                'create_time': detail['shf_goods_create_time'],
                'loading_time': loading_time
            }
            result.append({
                'priority': priority,
                'goods_type': goods_type,
                'content': '\n'.join([name, weight, volume]),
                'supplier_node': supplier_node,
                'address': '\n'.join([from_address, to_address, mileage_total]),
                'vehicle': vehicle,
                'price': '货主出价:%(price_expect)s元%(price_addition)s\n系统价:%(price_recommend)s元' % {
                    'price_expect': str(detail.get('price_expect', 0)),
                    'price_addition': '(+%s)' % str(detail['price_addition']) if detail.get('price_addition', 0) else '',
                    'price_recommend': detail.get('price_recommend', 0)
                },
                'mobile': detail.get('mobile', ''),
                'call_count': detail.get('call_count', 0),
                'goods_time': goods_time
            })
        data = json.loads(json.dumps(result))
        return build_result(APIStatus.Ok, count=goods_counts, data=result), HTTPStatus.Ok
