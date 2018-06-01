import time

from server import log
from server.meta.decorators import make_decorator
from server.status import build_result, APIStatus, HTTPStatus


class GoodsList(object):

    @staticmethod
    @make_decorator
    def get_result(data):

        goods_detail = data['goods_detail']
        # TODO 过滤参数
        try:
            for detail in goods_detail:

                # 网点
                detail['node_id'] = detail['node_id'] if detail.get('node_id') else "未知网点"

                # 货源类型
                if detail['haul_dist'] == 1 and detail['type'] == 1:
                    detail['goods_type'] = '同城'
                elif detail['haul_dist'] == 2 and detail['goods_level'] == 2 and detail['type'] == 1:
                    detail['goods_type'] = '跨城定价'
                elif detail['haul_dist'] == 2 and detail['goods_level'] == 1 and detail['type'] == 1:
                    detail['goods_type'] = '跨城议价'
                elif detail['type'] == 2:
                    detail['goods_type'] = '零担'
                else:
                    detail['goods_type'] = '未知货源类型'
                detail.pop('haul_dist')
                detail.pop('type')
                detail.pop('goods_level')

                # 构造货物规格
                goods_standard = []
                if detail['NAME']:
                    goods_standard.append(detail['NAME'])
                if detail['weight']:
                    goods_standard.append(detail['weight'] + '吨')
                if detail['volume']:
                    goods_standard.append(detail['volume'] + '㎡')
                detail['goods_standard'] = ','.join(goods_standard) if goods_standard else '没有规格'
                detail.pop('NAME')
                detail.pop('weight')
                detail.pop('volume')

                # TODO 优化 构造出发地-目的地-距离
                if detail['from_full_name'] and detail['from_address'] and detail['to_full_name'] \
                        and detail['to_address'] and detail['mileage_total']:
                    detail['from_to_dist'] = detail['from_full_name'] + detail['from_address'] + '到' + \
                                             detail['to_full_name'] + detail['to_address'] + ' ' + \
                                             detail['mileage_total'] + '㎞'
                if detail['from_full_name'] and detail['to_full_name'] and detail['mileage_total']:
                    detail['from_to_dist'] = detail['from_full_name'] + '到' + detail['to_full_name'] + ' ' + \
                                             detail['mileage_total'] + '㎞'
                elif detail['from_short_name'] and detail['to_short_name'] and detail['mileage_total']:
                    detail['from_to_dist'] = detail['from_short_name'] + '到' + detail['to_short_name'] + ' ' + \
                                             detail['mileage_total'] + '㎞'
                else:
                    detail['from_to_dist'] = '未知出发地和目的地，距离未知'
                detail.pop('from_full_name')
                detail.pop('to_full_name')
                detail.pop('from_short_name')
                detail.pop('to_short_name')
                detail.pop('from_address')
                detail.pop('to_address')
                detail.pop('mileage_total')

                # 构造装货时间
                if detail['loading_time_period_begin'] == 0:
                    loading_time_period = ''
                    if detail['loading_time_period'] == 0:
                        loading_time_period = '00:00:00'
                    if detail['loading_time_period'] == 1:
                        loading_time_period = '07:00:00'
                    if detail['loading_time_period'] == 2:
                        loading_time_period = '12:00:00'
                    if detail['loading_time_period'] == 3:
                        loading_time_period = '19:00:00'
                    detail['loading_time'] = detail['loading_time_date'] + ' ' + loading_time_period
                else:
                    detail['loading_time'] = time.strftime('%Y-%m-%d %H:%M:%S',
                                                           time.localtime(detail['loading_time_period_begin']))

                detail.pop('loading_time_period_begin')
                detail.pop('loading_time_date')
                detail.pop('loading_time_period')

            return build_result(APIStatus.Ok, count=data['goods_count'], data=goods_detail), HTTPStatus.Ok
        except Exception as e:
            log.error('Error:{}'.format(e))
