# -*- coding: utf-8 -*-

from server.meta.decorators import make_decorator
from server.status import build_result, HTTPStatus, APIStatus, make_result
from server.cache_data import init_regions
from server.logger import log
from server.utils.amap import distance

import time
from operator import itemgetter
import simplejson as json
from functools import reduce

class CityResourceBalance(object):
    @staticmethod
    @make_decorator
    def get_result(goods, vehicle, params):
        # 货源车型
        result = {}
        for i in goods:
            if i['new_vehicle'] in ['小面包车', '中面包车', '小货车', '4.2米', '6.8米', '7.6米', '9.6米', '13米', '17.5米']:
                vehicle_name = i['new_vehicle']
                result.setdefault(vehicle_name, {})
                if i['status'] == 3:
                    result[vehicle_name]['已接单'] = result[vehicle_name].setdefault('已接单', 0) + 1
                elif i['status'] == -1:
                    result[vehicle_name]['已取消'] = result[vehicle_name].setdefault('已取消', 0) + 1
                # 同城
                if params['goods_type'] == 1:
                    if i['status'] == 1 or i['status'] == 2:
                        result[vehicle_name]['待接单'] = result[vehicle_name].setdefault('待接单', 0) + 1
                # 跨城议价
                elif params['goods_type'] == 3:
                    if i['call_count'] == 0:
                        result[vehicle_name]['待联系'] = result[vehicle_name].setdefault('待联系', 0) + 1
                    else:
                        result[vehicle_name]['已联系'] =result[vehicle_name] .setdefault('已联系', 0) + 1
        # 接单车型
        for i in vehicle:
            if i['booking_vehicle'] in ['小面包车', '中面包车', '小货车', '4.2米', '6.8米', '7.6米', '9.6米', '13米', '17.5米']:
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
                    {'value': result[i].get('已接单', 0), 'name': '已接单'},
                    {'value': result[i].get('已取消', 0), 'name': '已取消'}
                ],
                # 内圈
                [
                    {'value': result[i].get('已接单车辆', 0), 'name': '已接单车辆'},
                    {'value': result[i].get('待接单车辆数', 0), 'name': '待接单车辆数'},
                ]
            ]
            if params['goods_type'] == 1:
                city_result[i][0].extend([{'value': result[i].get('待接单', 0), 'name': '待接单'},])
            elif params['goods_type'] == 3:
                city_result[i][0].extend([
                    {'value': result[i].get('待联系', 0), 'name': '待联系'},
                    {'value': result[i].get('已联系', 0), 'name': '已联系'}
                ])
            # 内圈空缺值
            city_result[i][1].append({'value': reduce(lambda x, y: x + y, [i['value'] for i in city_result[i][0]]) - reduce(lambda x, y: x + y, [i['value'] for i in city_result[i][1]]), 'name': '空缺', 'itemStyle': {
                'normal': {
                    'color': 'rgba(0,0,0,0)',
                    'label': {'show': False},
                    'labelLine': {'show': False}},
                'emphasis': {'color': 'rgba(0,0,0,0)'}}
             })
        return make_result(APIStatus.Ok, data=city_result), HTTPStatus.Ok


class CityOrderListFilterDecorator(object):

    @staticmethod
    @make_decorator
    def get_result(data):
        goods = data['goods_detail']
        goods_counts = data['goods_counts']
        result = []
        for detail in goods:
            # 新用户
            if detail['goods_counts'] <= 3:
                detail['mobile'] = detail.get('mobile', '') + '\n' + detail.get('user_name', '') + '\n新用户'
                new = 1
            else:
                detail['mobile'] = detail.get('mobile', '') + '\n' + detail.get('user_name', '') + '\n'
                new = 0

            # # 紧急 now（）-发布时间 < 10分钟
            # if time.time() - detail['create_time'] <= 300:
            #     urgent = 1
            # else:
            #     urgent = 0

            # 货源距离类型
            if detail['haul_dist'] == 1:
                goods_type = '同城'
            elif detail['haul_dist'] == 2:
                goods_type = '跨城'
            elif detail['type'] == 2:
                goods_type = '零担'
            else:
                goods_type = '未知货源类型'

            # 货源距离类型
            if detail['is_system_price'] == 0:
                goods_type += '议价'
            elif detail['is_system_price'] == 1:
                goods_type += '一口价'
            else:
                goods_type += ''

            # 货物规格
            name = detail.get('name', '')
            weight = str(int(detail['weight'] * 1000)) + '千克' if 0 < detail.get('weight', 0) < 1 else str(int(detail.get('weight', 0))) + '吨'
            volume = str(int(detail.get('volume', 0))) + 'm³'
            # 网点
            supplier_node = init_regions.to_address(detail.get('from_province_id', 0), detail.get('from_city_id', 0),
                                                  detail.get('from_county_id', 0))
            # 出发地-目的地
            from_address = init_regions.to_address(detail.get('from_province_id', 0), detail.get('from_city_id', 0),
                                                  detail.get('from_county_id', 0)) + detail.get('from_address', '无详细地址')
            to_address = init_regions.to_address(detail.get('to_province_id', 0), detail.get('to_city_id', 0),
                                                  detail.get('to_county_id', 0)) + detail.get('to_address', '无详细地址')
            mileage_total = str(int(detail['mileage_total'] * 1000)) + 'm'\
                if 0 < detail.get('mileage_total', 0) < 1 else str(int(detail.get('mileage_total', 0))) + 'km'
            # 特殊车型
            extra = [
                '需要开顶' if detail['need_open_top'] == 1 else '',
                '需要尾板' if detail['need_tail_board'] == 1 else '',
                '需要平板' if detail['need_flatbed'] == 1 else '',
                '需要高栏' if detail['need_high_sided'] == 1 else '',
                '需要箱式' if detail['need_box'] == 1 else '',
                '需要钢板车' if detail['need_steel'] == 1 else '',
                '需要双排座' if detail['need_double_seat'] == 1 else '',
                '需要全拆座' if detail['need_remove_seat'] == 1 else ''
            ]
            extra = [i for i in extra if i != '']
            # 车长+特殊要求
            if detail['new_vehicle_type']:
                L = [detail['new_vehicle_type']] + extra
                vehicle = '\n'.join(L)
            else:
                vehicle_type = detail['vehicle_type'] if detail['vehicle_type'] else ''
                L = [vehicle_type] + extra
                vehicle = '\n'.join(L)
            # 发布、装货时间
            if detail['loading_time_period_end']:
                loading_time = detail['shf_goods_loading_time_period_end']
            else:
                if detail['loading_time_period'] == 1:
                    loading_time = detail.get('loading_time_date', '') + ' 08:00:00'
                elif detail['loading_time_period'] == 2:
                    loading_time = detail.get('loading_time_date', '') + ' 13:00:00'
                elif detail['loading_time_period'] == 3:
                    loading_time = detail.get('loading_time_date', '') + ' 19:00:00'
                else:
                    loading_time = detail.get('loading_time_date', '') + ' 00:00:00'
            goods_time = '%(create_time)s\n%(loading_time)s' % {
                'create_time': detail['shf_goods_create_time'],
                'loading_time': loading_time
            }
            result.append({
                'goods_id': detail.get('id', 0),
                # 'priority': priority,
                'goods_type': goods_type,
                'content': '\n'.join([name, weight, volume]),
                'supplier_node': supplier_node,
                'address': '\n'.join([from_address, to_address, mileage_total]),
                'vehicle': vehicle,
                'price': '货主出价:%(price_expect)s元%(price_addition)s\n系统价:%(price_recommend)s元' % {
                    'price_expect': str(int(detail.get('price_expect', 0) + detail.get('price_addition', 0))),
                    'price_addition': '(+%s)' % str(int(detail['price_addition'])) if detail.get('price_addition') else '',
                    'price_recommend': str(int(detail.get('price_recommend', 0)))
                },
                'mobile': detail.get('mobile', ''),
                'call_count': detail.get('call_count', 0),
                'goods_time': goods_time,

                # 排序条件
                # 'priority_num': priority_num,
                'new': new,
                # 'urgent': urgent,
                # 'price_addition': int(detail['price_addition']) if detail.get('price_addition', 0) else 0,
                'create_time': detail['create_time']
            })

        # 排序
        # 第一层排序：带有“新用户“
        # 第二层排序：发布时间倒序
        ret = sorted(result, key=itemgetter('new', 'create_time'), reverse=True)

        data = json.loads(json.dumps(ret))
        return build_result(APIStatus.Ok, count=goods_counts, data=data), HTTPStatus.Ok


class CityNearbyCars(object):

    @staticmethod
    @make_decorator
    def get_result(data, goods_type):
        try:
            if not data:
                return make_result(APIStatus.Ok, data=[]), HTTPStatus.Ok
            goods = data['goods']
            driver = data['driver']
            # 过滤接单车型
            if goods_type == 1:
                booking_vehicle = driver
                town = []
                count = []
                for i in booking_vehicle:
                    if i['from_town_id'] != 0 and i['to_town_id'] != 0 and goods['from_town_id'] == i[
                        'from_town_id'] and goods['to_town_id'] == i['to_town_id']:
                        town.append(i)
                        booking_vehicle.pop(i)
                    elif i['from_town_id'] != 0 and i['to_town_id'] != 0 and goods['from_town_id'] == i[
                        'from_town_id'] and goods['to_town_id'] == i['to_town_id']:
                        count.append(i)
                        booking_vehicle.pop(i)
                driver = (town + count + booking_vehicle)[:10]
            result = []
            # 常驻地
            if goods_type == 2:
                for i in driver:
                    # 时间间隔
                    last_delta = i['last_delta']
                    delta = ''
                    if last_delta // 86400 > 0:
                        delta = '%d天前' % (last_delta // 86400)
                    elif last_delta // 3600 > 0:
                        delta = '%d小时前' % (last_delta // 3600)
                    elif last_delta // 60 > 0:
                        delta = '%d分钟前' % (last_delta // 60)
                    usual_region = init_regions.to_address(i['from_province_id'], i['from_city_id'],
                                                           i['from_county_id'])
                    locations = init_regions.to_address(i['province'], i['city'], i['county']) + i['address'] + ', ' + \
                                i['last_login_time'] + ', ' + delta
                    result.append({
                        'name': i['user_name'],
                        'mobile': i['mobile'],
                        'usual_region': usual_region,
                        'locations': locations,
                        'vehicle_length': i['vehicle_length_id'],
                        'is_trust_member': i['is_sticker'],
                        'order_count': i['order_count'],
                        'order_finished': i['order_finished'],
                        'order_cancel': i['order_cancel'],
                        'last_login_time': i['last_login_time']
                    })
                    if len(result) >= 10:
                        break

                result.sort(key=lambda x: x.get('last_login_time', 0))
            else:
                for i in driver:
                    # 诚信会员
                    is_trust_member = 0
                    if i['trust_member_type'] == 1:
                        is_trust_member = 1
                    elif i['trust_member_type'] == 2 and i['ad_expired_time'] > int(time.time()):
                        is_trust_member = 1
                    result.append({
                        'name': i['user_name'],
                        'mobile': i['mobile'],
                        'booking_line': init_regions.to_address(i['from_province_id'], i['from_city_id'],
                                                                i['from_county_id']) + '-' + init_regions.to_address(
                            i['to_province_id'], i['to_city_id'], i['to_county_id']),
                        'booking_time': i['create_time'] if i['create_time'] else '',
                        'last_login_time': time.strftime('%Y-%m-%d', time.localtime(i['last_login_time'])),
                        'vehicle_length': i['vehicle_length'] if i['vehicle_length'] else '',
                        'is_trust_member': is_trust_member,
                        'order_count': i['order_count'],
                        'order_finished': i['order_finished'],
                        'order_cancel': i['order_cancel'],
                    })
                    if len(result) >= 10:
                        break
                result.sort(key=lambda x: x.get('booking_time', ''), reverse=True)
            return make_result(APIStatus.Ok, data=json.loads(json.dumps(result))), HTTPStatus.Ok
        except Exception as e:
            log.error('附近车辆过滤错误: %s' % e, exc_info=True)