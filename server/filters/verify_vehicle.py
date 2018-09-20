from server.cache_data import init_regions
from server.meta.decorators import make_decorator
from server.status import APIStatus, HTTPStatus, make_resp
from server.utils.constant import vehicle_id_name


class VerifyVehicle(object):

    @staticmethod
    @make_decorator
    def get_result(data):
        verify_vehicle_list = data['verify_vehicle_list']
        result = []
        for detail in verify_vehicle_list:
            # 常驻地
            home_station = init_regions.to_address(detail.get('home_station_province_id', 0),
                                                   detail.get('home_station_city_id', 0),
                                                   detail.get('home_station_county_id', 0)) + \
                           init_regions.to_region(detail.get('home_station_town_id', 0))
            # 车长/车型名称
            vehicle_length_type = (detail.get('length_name') or '') + '/' + (detail.get('type_name') or '')

            result.append({
                'id': detail.get('id') or 0,
                'name': detail.get('user_name') or '',
                'mobile': detail.get('mobile') or '',
                'number': detail.get('number') or '',
                'home_station': home_station,
                'vehicle_length_type': vehicle_length_type,
                'audit_time': detail.get('audit_time') or '',
                'last_login_time': detail.get('last_login_time') or '',
            })

        return make_resp(APIStatus.Ok, data=result, count=data['count']), HTTPStatus.Ok
