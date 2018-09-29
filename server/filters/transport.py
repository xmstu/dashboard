import json
import time

from flask_restful import abort

from server import log
from server.cache_data import init_regions
from server.meta.decorators import make_decorator
from server.status import make_resp, APIStatus, HTTPStatus, make_resp
from server.utils.extend import ExtendHandler, date2timestamp


class TransportList(object):

    @staticmethod
    @make_decorator
    def get_result(params, data):
        try:
            transport_list = data['transport_list']
            general_situation = filter_fields(params, data["general_situation"])
            result = filter_fields(params, transport_list)
            return make_resp(APIStatus.Ok, data=result, count=data['count'], general_situation=general_situation), HTTPStatus.Ok
        except Exception as e:
            log.error('TransportListFilter Error:{}'.format(e), exc_info=True)
            abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='过滤参数时有误'))


def filter_fields(params, data):
    result = []
    for detail in data:
        # 出发地-目的地
        from_address = init_regions.to_city(detail['from_city_id']) + \
                       init_regions.to_county(detail.get('from_county_id', 0))
        to_address = init_regions.to_city(detail['to_city_id']) + init_regions.to_county(detail.get('to_county_id', 0))

        result.append({
            'from_address': from_address,
            'to_address': to_address,
            'login_driver_count': detail.get('login_driver_count', 0),
            'total_driver_count': detail.get('total_driver_count', 0),
            'from_city_id': detail.get('from_city_id', 0),
            'from_county_id': detail.get('from_county_id', 0),
            'to_city_id': detail.get('to_city_id', 0),
            'to_county_id': detail.get('to_county_id', 0),

            'start_time': params['start_time'],
            'end_time': int(time.time())
        })
    return result
