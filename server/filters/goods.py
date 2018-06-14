import calendar
import datetime
import json
import time

from flask_restful import abort

from server import log
from server.init_regions import init_regions
from server.meta.decorators import make_decorator
from server.status import build_result, APIStatus, HTTPStatus, make_result


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
                            'price_addition': '(+%s)' % str(detail['price_addition']) if detail.get('price_addition', 0) else '+0',
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

        # 结构化数据
        date_count = {}
        for count in data:
            if count.get('create_time'):
                date_count[count['create_time'].strftime('%Y-%m-%d')] = count.get('count', 0)
        # 日期补全
        begin_date = datetime.datetime.strptime(time.strftime("%Y-%m-%d", time.localtime(params['start_time'])), "%Y-%m-%d")
        end_date = datetime.datetime.strptime(time.strftime("%Y-%m-%d", time.localtime(params['end_time'])), "%Y-%m-%d")

        # 日
        xAxis = []
        series = []
        if params['periods'] == 2:
            date_val = begin_date
            while date_val <= end_date:
                date_str = date_val.strftime("%Y-%m-%d")
                date_count.setdefault(date_str, 0)
                xAxis.append(date_str)
                series.append(date_count[date_str])
                date_val += datetime.timedelta(days=1)
        # 周
        elif params['periods'] == 3:
            begin_flag = begin_date
            end_flag = begin_date
            count = 0
            sum_count = 0
            while end_flag <= end_date:
                date_str = end_flag.strftime("%Y-%m-%d")
                sum_count += date_count.get(date_str, 0)
                date_count.setdefault(date_str, sum_count)
                # 本周结束
                if count == 6:
                    xAxis.append(begin_flag.strftime('%Y/%m/%d') + '-' + end_flag.strftime('%Y/%m/%d'))
                    series.append(sum_count)
                    begin_flag = end_flag + datetime.timedelta(days=1)
                    sum_count = 0
                    count = 0
                if end_flag == end_date:
                    xAxis.append(begin_flag.strftime('%Y/%m/%d') + '-' + end_flag.strftime('%Y/%m/%d'))
                    series.append(sum_count)
                    begin_flag = end_flag + datetime.timedelta(days=1)
                    sum_count = 0
                    count = 0
                end_flag += datetime.timedelta(days=1)
                count += 1
        # 月
        elif params['periods'] == 4:
            begin_flag = begin_date
            end_flag = begin_date
            sum_count = 0
            while end_flag <= end_date:
                date_str = end_flag.strftime("%Y-%m-%d")
                sum_count += date_count.get(date_str, 0)
                month_lastweek, month_lastday = calendar.monthrange(begin_flag.year, begin_flag.month)
                # 结束日期
                if end_flag == end_date:
                    xAxis.append(begin_flag.strftime('%Y/%m/%d') + '-' + end_date.strftime('%Y/%m/%d'))
                    series.append(sum_count)
                else:
                    # 本月结束
                    if end_flag.day == month_lastday and end_flag.month == begin_flag.month:
                        xAxis.append(begin_flag.strftime('%Y/%m/%d') + '-' + end_flag.strftime('%Y/%m/%d'))
                        series.append(sum_count)
                        begin_flag = end_flag + datetime.timedelta(days=1)
                        sum_count = 0
                end_flag += datetime.timedelta(days=1)

        return make_result(APIStatus.Ok, data=data), HTTPStatus.Ok