from server.cache_data import init_regions
from server.meta.decorators import make_decorator
from server.status import build_result, APIStatus, HTTPStatus


class RootManagement(object):

    @staticmethod
    @make_decorator
    def get_result(data):
        city_manager_list = data.get('city_manager_list')
        for detail in city_manager_list:
            region_name = init_regions.to_region(detail.get('region_id'))
            detail['region_name'] = region_name

        return build_result(APIStatus.Ok, data=city_manager_list, count=data.get('count', 0)), HTTPStatus.Ok