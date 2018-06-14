import json

from flask_restful import abort

from server import log
from server.init_regions import init_regions
from server.meta.decorators import make_decorator
from server.status import build_result, APIStatus, HTTPStatus, make_result
from server.utils.extend import get_struct_data, get_xAxis


class GoodsList(object):

    @staticmethod
    @make_decorator
    def get_result(data):
        goods_detail = data['goods_detail']
        try:
            result = []
            for detail in goods_detail:

                # 构造货源状态
                if detail.get('expire'):
                    detail['goods_status'] = '已过期'
                    if detail.get('STATUS') in (1, 2):
                        detail['goods_status'] += ',待接单'
                    if detail.get('STATUS') == 3:
                        detail['goods_status'] += ',已接单'
                    if detail.get('STATUS') == -1:
                        detail['goods_status'] += ',已取消'
                else:
                    if detail.get('STATUS') in (1, 2):
                        detail['goods_status'] = '待接单'
                    if detail.get('STATUS') == 3:
                        detail['goods_status'] = '已接单'
                    if detail.get('STATUS') == -1:
                        detail['goods_status'] = '已取消'
                goods_status = detail['goods_status']

                # 初次下单
                mobile = detail['mobile']
                if detail['shf_goods_counts'] == 1:
                    mobile = detail['mobile'] + ',初次下单'

                # 构造运费
                price = '货主出价:%(price_expect)s元%(price_addition)s元\n系统价:%(price_recommend)s元' % \
                        {
                            'price_expect': str(detail.get('price_expect', 0)),
                            'price_addition': '(+%s)' % str(detail['price_addition']) if detail.get('price_addition',
                                                                                                    0) else '+0',
                            'price_recommend': str(detail.get('price_recommend', 0))
                        }

                # 网点
                node_id = init_regions.to_address(detail.get('from_province_id', 0), detail.get('from_city_id', 0),
                                                  detail.get('from_county_id', 0))

                # 货源类型
                if detail['haul_dist'] == 1 and detail['type'] == 1:
                    goods_type = '同城'
                elif detail['haul_dist'] == 2 and detail['goods_level'] == 2 and detail['type'] == 1:
                    goods_type = '跨城定价'
                elif detail['haul_dist'] == 2 and detail['goods_level'] == 1 and detail['type'] == 1:
                    goods_type = '跨城议价'
                elif detail['type'] == 2:
                    goods_type = '零担'
                else:
                    goods_type = '未知货源类型'

                # 构造货物规格
                goods_standard = []
                if detail['NAME']:
                    goods_standard.append(detail['NAME'])
                if detail['weight']:
                    weight = str(int(detail['weight'] * 1000)) + '千克' \
                        if detail.get('weight', 0) < 1 and detail.get('weight', 0) > 0 \
                        else str(int(detail.get('weight', 0))) + '吨'
                    goods_standard.append(weight)
                if detail['volume']:
                    volume = str(int(detail.get('volume', 0))) + '平米'
                    goods_standard.append(volume)

                goods_standard = '\n'.join(goods_standard) if goods_standard else '没有规格'

                # 出发地-目的地
                from_address = init_regions.to_address(detail.get('from_province_id', 0), detail.get('from_city_id', 0),
                                                       detail.get('from_county_id', 0)) + detail.get('from_address',
                                                                                                     '无详细地址')
                to_address = init_regions.to_address(detail.get('to_province_id', 0), detail.get('to_city_id', 0),
                                                     detail.get('to_county_id', 0)) + detail.get('to_address', '无详细地址')
                mileage_total = str(int(detail['mileage_total'] * 1000)) + '米' \
                    if detail.get('mileage_total', 0) < 1 and detail.get('mileage_total', 0) > 0 \
                    else str(int(detail.get('mileage_total', 0))) + '千米'

                address = '\n'.join([from_address, to_address, mileage_total])

                # 车长、车型
                if detail['new_vehicle_type'] and detail['new_vehicle_length']:
                    vehicle = '\n'.join([detail['new_vehicle_type'], detail['new_vehicle_length']])
                else:
                    vehicle = '\n'

                # 发布、装货时间
                if detail['loading_time_period_begin']:
                    loading_time = detail['loading_time_period_begin']
                else:
                    if detail['loading_time_period'] == 1:
                        loading_time = detail.get('loading_time_date', '') + '08:00:00'
                    elif detail['loading_time_period'] == 2:
                        loading_time = detail.get('loading_time_date', '') + '13:00:00'
                    elif detail['loading_time_period'] == 3:
                        loading_time = detail.get('loading_time_date', '') + '19:00:00'
                    else:
                        loading_time = detail.get('loading_time_date', '') + '00:00:00'
                goods_time = '发布时间:%(create_time)s\n装货时间:%(loading_time)s' % {
                    'create_time': detail['shf_goods_create_time'],
                    'loading_time': loading_time
                }

                result.append({
                    'id': detail['id'],
                    'mobile': mobile,
                    'shf_goods_counts': detail['shf_goods_counts'],
                    'call_count': detail['call_count'],
                    'goods_status': goods_status,
                    'price': price,
                    'node_id': node_id,
                    'goods_type': goods_type,
                    'goods_standard': goods_standard,
                    'address': address,
                    'vehicle': vehicle,
                    'goods_time': goods_time,
                })

            result = json.loads(json.dumps(result))
            return build_result(APIStatus.Ok, count=data['goods_count'], data=result), HTTPStatus.Ok
        except Exception as e:
            log.error('Error:{}'.format(e))
            abort(HTTPStatus.BadRequest, **make_result(HTTPStatus.BadRequest, msg='内部服务器错误'))


class CancelGoodsReason(object):

    @staticmethod
    @make_decorator
    def get_result(data):
        pass
        return make_result(APIStatus.Ok, data=data), HTTPStatus.Ok


class GoodsDistributionTrend(object):

    @staticmethod
    @make_decorator
    def get_result(data, params):
        wait_order = data['wait_order']
        recv_order = data['recv_order']
        cancel_order = data['cancel_order']

        goods_user_count_series = get_struct_data(wait_order, params, 'goods_user_count')
        wait_order_series = get_struct_data(wait_order, params, 'count')
        recv_order_series = get_struct_data(recv_order, params, 'count')
        cancel_order_series = get_struct_data(cancel_order, params, 'count')

        xAxis = get_xAxis(params)

        ret = {
            'xAxis': xAxis,
            'wait_order_series': wait_order_series,
            'recv_order_series': recv_order_series,
            'cancel_order_series': cancel_order_series,
            'goods_user_count_series': goods_user_count_series
        }
        return make_result(APIStatus.Ok, data=ret), HTTPStatus.Ok
