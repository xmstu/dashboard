import json

from flask_restful import abort

from server import log
from server.cache_data import init_regions
from server.meta.decorators import make_decorator
from server.status import make_result, APIStatus, HTTPStatus, build_result
from server.utils.extend import ExtendHandler, date2timestamp


class TransportRadar(object):

    @staticmethod
    @make_decorator
    def get_result(data):
        # TODO 过滤参数

        return make_result(APIStatus.Ok, data=data), HTTPStatus.Ok


class TransportList(object):

    @staticmethod
    @make_decorator
    def get_result(data):
        try:
            data = json.loads(json.dumps(data, default=ExtendHandler.handler_to_float))
            transport_list = data['transport_list']
            result = []
            for detail in transport_list:
                # 业务类型
                business = '未知业务'
                if detail.get('haul_dist') == 1:
                    business = '同城'
                elif detail.get('haul_dist') == 2:
                    business = '跨城'

                # 出发地-目的地
                from_address = init_regions.to_address(detail.get('from_province_id', 0), detail.get('from_city_id', 0),
                                                       detail.get('from_county_id', 0)) + init_regions.to_town(
                    detail.get('from_town_id', 0))
                to_address = init_regions.to_address(detail.get('to_province_id', 0), detail.get('to_city_id', 0),
                                                     detail.get('to_county_id', 0)) + init_regions.to_town(
                    detail.get('to_town_id', 0))

                result.append({
                    'business': business,
                    'from_address': from_address,
                    'to_address': to_address,
                    'mileage': "%.2fkm" % detail.get('avg_mileage_total', 0.0),
                    'goods_count': detail.get('goods_count', None) or 0,
                    'order_count': detail.get('order_count', None) or 0,
                    'vehicle_count': detail.get('vehicle_count', None) or 0,
                    'create_time': detail.get('create_time', '时间不详'),
                    # 前端要用的字段
                    'haul_dist': detail.get('haul_dist'),
                    'from_province_id': detail.get('from_province_id', 0),
                    'from_city_id': detail.get('from_city_id', 0),
                    'from_county_id': detail.get('from_county_id', 0),
                    'from_town_id': detail.get('from_town_id', 0),
                    'to_province_id': detail.get('to_province_id', 0),
                    'to_city_id': detail.get('to_city_id', 0),
                    'to_county_id': detail.get('to_county_id', 0),
                    'to_town_id': detail.get('to_town_id', 0),
                    'begin_time': date2timestamp(detail['create_time'], accuracy=2),
                    'end_time': date2timestamp(detail['create_time'], accuracy=2) + 86399
                })

            return build_result(APIStatus.Ok, data=result, count=data['count']), HTTPStatus.Ok
        except Exception as e:
            log.error('TransportListFilter Error:{}'.format(e))
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='过滤参数时有误'))

