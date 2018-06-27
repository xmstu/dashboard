import json

from flask_restful import abort

from server import log
from server.cache_data import init_regions
from server.meta.decorators import make_decorator
from server.status import make_result, APIStatus, HTTPStatus, build_result
from server.utils.extend import ExtendHandler, get_struct_data, get_xAxis, timestamp2date


class OrdersReceivedStatistics(object):

    @staticmethod
    @make_decorator
    def get_result(data, params):
        complete_order_count_series = get_struct_data(data['complete_order'], params, 'order_counts')
        complete_order_sum_price_series = get_struct_data(data['complete_order'], params, 'order_sum_price')

        pending_order_count_series = get_struct_data(data['pending_order'], params, 'order_counts')
        pending_order_sum_price_series = get_struct_data(data['pending_order'], params, 'order_sum_price')

        cancel_order_count_series = get_struct_data(data['cancel_order'], params, 'order_counts')
        cancel_order_sum_price_series = get_struct_data(data['cancel_order'], params, 'order_sum_price')

        xAxis = get_xAxis(params['periods'], params['start_time'], params['end_time'])

        complete_order_count_series = json.loads(json.dumps(complete_order_count_series, default=ExtendHandler.handler_to_float))
        pending_order_count_series = json.loads(json.dumps(pending_order_count_series, default=ExtendHandler.handler_to_float))
        cancel_order_count_series = json.loads(json.dumps(cancel_order_count_series, default=ExtendHandler.handler_to_float))

        complete_order_sum_price_series = json.loads(json.dumps(complete_order_sum_price_series, default=ExtendHandler.handler_to_float))
        pending_order_sum_price_series = json.loads(json.dumps(pending_order_sum_price_series, default=ExtendHandler.handler_to_float))
        cancel_order_sum_price_series = json.loads(json.dumps(cancel_order_sum_price_series, default=ExtendHandler.handler_to_float))

        if params.get('dimension') == 1:
            complete_series = complete_order_count_series
            pending_series = pending_order_count_series
            cancel_series = cancel_order_count_series
        elif params.get('dimension') == 2:
            complete_series = complete_order_sum_price_series
            pending_series = pending_order_sum_price_series
            cancel_series = cancel_order_sum_price_series
        else:
            complete_series = [0 for _ in xAxis]
            pending_series = [0 for _ in xAxis]
            cancel_series = [0 for _ in xAxis]

        ret = {
            'xAxis': xAxis,
            'complete_series': complete_series,
            'pending_series': pending_series,
            'cancel_series': cancel_series
        }
        return make_result(APIStatus.Ok, data=ret), HTTPStatus.Ok


class CancelOrderReason(object):

    @staticmethod
    @make_decorator
    def get_result(data):
        # TODO 过滤参数

        return make_result(APIStatus.Ok, data=data), HTTPStatus.Ok


class OrderList(object):

    @staticmethod
    @make_decorator
    def get_result(data, params):
        order_list = data['order_list']
        try:
            result = []
            for detail in order_list:
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
                    volume = str(int(detail.get('volume', 0))) + 'm³'
                    goods_standard.append(volume)

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

                # 网点
                supplier_node = init_regions.to_address(detail.get('from_province_id', 0),
                                                        detail.get('from_city_id', 0),
                                                        detail.get('from_county_id', 0))
                # 出发地-目的地
                from_address = init_regions.to_address(detail.get('from_province_id', 0), detail.get('from_city_id', 0),
                                                       detail.get('from_county_id', 0)) + detail.get('from_address',
                                                                                                     '无详细地址')
                to_address = init_regions.to_address(detail.get('to_province_id', 0), detail.get('to_city_id', 0),
                                                     detail.get('to_county_id', 0)) + detail.get('to_address', '无详细地址')
                mileage_total = str(int(detail['mileage_total'] * 1000)) + '米' \
                    if 0 < detail.get('mileage_total', 0) < 1 else str(int(detail.get('mileage_total', 0))) + '千米'
                address = '\n'.join([from_address, to_address, mileage_total])

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

                # 构造运费
                freight = '{0}'.format(str(detail['price']))

                # 构造货主字段
                cargo_owner = '\n'.join([str(detail['owner_mobile']), str(detail['owner_name']), '新货主' if detail['c2'] < 3 else ''])

                # 构造司机字段
                driver = '\n'.join([str(detail['driver_mobile']), str(detail['driver_name']), '新司机' if detail['c1'] < 3 else ''])

                # 订单状态
                if detail['status'] not in (0, -1) and detail['pay_status'] == 1 and detail['paid_offline'] == 0:
                    order_status = '已接单'
                elif detail['status'] == 3 and (detail['pay_status'] == 2 or detail['paid_offline'] == 1):
                    order_status = '已完成'
                elif detail['status'] == -1:
                    order_status = '已取消'
                else:
                    order_status = ''

                order_status += '\n'

                if detail['pay_status'] == 1 and detail['paid_offline'] == 0:
                    order_status += '未支付'
                elif detail['pay_status'] == 2:
                    order_status += '线上支付'
                elif detail['paid_offline'] == 1:
                    order_status += '线下支付'
                else:
                    order_status += ''

                if detail['level'] in (1, 2):
                    evaluation = '差评'
                elif detail['level'] == 3:
                    evaluation = '中评'
                elif detail['level'] in (4, 5):
                    evaluation = '好评'
                else:
                    evaluation = '未评价'

                result.append({
                    'order_id': detail['id'],
                    'goods_standard': '\n'.join(goods_standard),
                    'goods_type': goods_type,
                    'supplier_node': supplier_node,
                    'address': address,
                    'vehicle': vehicle,
                    'freight': freight,
                    'cargo_owner': cargo_owner,
                    'driver': driver,
                    'order_status': order_status,
                    'evaluation': evaluation,
                    'complete_time': timestamp2date(detail['complete_time'], 2) if detail['complete_time'] else '待完成',
                    'create_time': timestamp2date(detail['create_time'], 2) if detail['create_time'] else '未知接单时间',
                    'latency_time': "%.2f分钟" % (detail['latency_time'] / 60)
                })

            return build_result(APIStatus.Ok, count=data['count'], data=result), HTTPStatus.Ok
        except Exception as e:
            log.error('Error:{}'.format(e))
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='请求参数有误'))


