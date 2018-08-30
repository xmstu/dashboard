from server.cache_data import init_regions
from server.meta.decorators import make_decorator
from server.status import make_result, APIStatus, HTTPStatus, build_result
from server.utils.date_format import get_date_aggregate
from server.utils.extend import timestamp2date, interval_time_to_format_time


class GoodsPotentialDistributionTrend(object):

    @staticmethod
    @make_decorator
    def get_result(data, params):
        # 过滤参数
        xAxis, series = get_date_aggregate(params['start_time'], params['end_time'], params['periods'], data)
        ret = {
            'xAxis': xAxis,
            'series': series
        }
        return make_result(APIStatus.Ok, data=ret), HTTPStatus.Ok


class GoodsPotentialList(object):

    @staticmethod
    @make_decorator
    def get_result(data):
        # 过滤参数
        potential_data = data.get('potential_data')
        result = []
        for detail in potential_data:
            # 构造货物规格
            goods_standard = []
            if detail['name']:
                goods_standard.append(detail['name'])
            if detail['weight']:
                weight = str(int(detail['weight'] * 1000)) + '千克' \
                    if detail.get('weight', 0) < 1 and detail.get('weight', 0) > 0 \
                    else str(int(detail.get('weight', 0))) + '吨'
                goods_standard.append(weight)
            if detail['volume']:
                volume = str(int(detail.get('volume', 0))) + 'm³'
                goods_standard.append(volume)

            goods_standard = '\n'.join(goods_standard) if goods_standard else '没有规格'

            # 零担货源类型
            if detail.get('goods_type'):
                goods_type = detail['goods_type']
            else:
                # 整车货源类型
                if detail['is_system_price'] == 0:
                    goods_type = '议价'
                elif detail['is_system_price'] == 1:
                    goods_type = '一口价'
                else:
                    goods_type = ''

                goods_type += '\n'

                # 货源距离类型
                if detail['haul_dist'] == 1:
                    goods_type += '同城'
                elif detail['haul_dist'] == 2:
                    goods_type += '跨城'
                else:
                    goods_type += '未知货源类型'

            # 出发地-目的地
            from_address = init_regions.to_address(detail.get('from_province_id', 0),
                                                   detail.get('from_city_id', 0),
                                                   detail.get('from_county_id', 0)) + detail.get('from_address',
                                                                                                 '无详细地址')
            to_address = init_regions.to_address(detail.get('to_province_id', 0), detail.get('to_city_id', 0),
                                                 detail.get('to_county_id', 0)) + detail.get('to_address',
                                                                                             '无详细地址')
            if detail.get('mileage_total'):
                mileage_total = str(int(detail['mileage_total'] * 1000)) + 'm' \
                    if detail.get('mileage_total', 0) < 1 and detail.get('mileage_total', 0) > 0 \
                    else str(int(detail.get('mileage_total', 0))) + 'km'
            else:
                mileage_total = ''
            address = '\n'.join([from_address, to_address, mileage_total])

            # 车长+特殊要求
            if detail['vehicle_name']:
                # 特殊车型
                extra = [
                    '需要开顶' if detail.get('need_open_top') == 1 else '',
                    '需要尾板' if detail.get('need_tail_board') == 1 else '',
                    '需要平板' if detail.get('need_flatbed') == 1 else '',
                    '需要高栏' if detail.get('need_high_sided') == 1 else '',
                    '需要箱式' if detail.get('need_box') == 1 else '',
                    '需要钢板车' if detail.get('need_steel') == 1 else '',
                    '需要双排座' if detail.get('need_double_seat') == 1 else '',
                    '需要全拆座' if detail.get('need_remove_seat') == 1 else ''
                ]
                extra = [i for i in extra if i != '']
                L = [detail['vehicle_name']] + extra
                vehicle = '\n'.join(L)
            else:
                vehicle = '-'

            # 初次下单
            mobile = detail['mobile']
            if detail['goods_counts'] < 3:
                mobile = mobile + '\n' + detail.get('user_name', '') + '\n新用户'
            else:
                mobile = mobile + '\n' + detail.get('user_name', '') + '\n'

            if detail.get('stay_time'):
                stay_time = interval_time_to_format_time(detail['stay_time'])
            else:
                stay_time = '-'

            result.append({
                'goods_standard': goods_standard,
                'goods_type': goods_type,
                'address': address,
                'vehicle': vehicle,
                'price': str(detail.get('price', 0)) + '元',
                'mobile': mobile,
                'goods_counts': detail.get('goods_counts'),
                'orders_counts': detail.get('orders_counts'),
                'stay_time': stay_time,
                'query_time': timestamp2date(detail.get('query_time'), accuracy=2),
                'register_time': detail.get('register_time')
            })

        return build_result(APIStatus.Ok, count=data.get('count'), data=result), HTTPStatus.Ok