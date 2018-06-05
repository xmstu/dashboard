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
        # TODO 过滤参数
        try:
            for detail in goods_detail:

                # 初次下单
                if detail['shf_goods_counts'] == 1:
                    detail['mobile'] = detail['mobile'] + ',初次下单'

                # 构造运费
                detail['fee'] = detail.get('price_expect', 0) + ',' + detail.get('price_addition',
                                                                                 0) + ',' + detail.get(
                    'price_recommend', 0)
                detail.pop('price_expect')
                detail.pop('price_addition')
                detail.pop('price_recommend')

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
                full_from_region_name = init_regions.to_province(
                    detail['from_province_id']) + init_regions.to_city(detail['from_city_id']) + init_regions.to_county(
                    detail['from_county_id']) + init_regions.to_town(detail['from_town_id']) + detail['from_address'] if detail.get('from_address') else ''

                full_to_region_name = init_regions.to_province(
                    detail['to_province_id']) + init_regions.to_city(
                    detail['to_city_id']) + init_regions.to_county(detail['to_county_id']) + init_regions.to_town(detail['to_town_id']) + detail['to_address'] if detail.get('to_address') else ''

                detail['from_to_dis'] = full_from_region_name + ',' + full_to_region_name + ',' + detail['mileage_total'] if detail.get('mileage_total') else 0

                detail.pop('from_province_id')
                detail.pop('from_city_id')
                detail.pop('from_county_id')
                detail.pop('from_town_id')
                detail.pop('from_address')
                detail.pop('to_province_id')
                detail.pop('to_city_id')
                detail.pop('to_county_id')
                detail.pop('to_town_id')
                detail.pop('to_address')

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
            abort(HTTPStatus.BadRequest, **make_result(HTTPStatus.BadRequest, msg='内部服务器错误'))
