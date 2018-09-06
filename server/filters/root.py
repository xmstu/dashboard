from server.cache_data import init_regions
from server.meta.decorators import make_decorator
from server.status import build_result, APIStatus, HTTPStatus


class RootManagement(object):

    @staticmethod
    @make_decorator
    def get_result(data):
        city_manager_list = data.get('city_manager_list')
        for detail in city_manager_list:
            if detail.get('is_deleted') == 0:
                detail['status'] = '启用'
            elif detail.get('is_deleted') == 1:
                detail['status'] = '禁用'
            detail.pop('is_deleted')

        return build_result(APIStatus.Ok, data=city_manager_list, count=data.get('count', 0)), HTTPStatus.Ok


class RootRoleManagement(object):

    @staticmethod
    @make_decorator
    def get_result(data):
        role_list = data.get('role_list')
        for i in role_list:
            if i['region_id'] == 1:
                i['region_name'] = '全国'
            else:
                i['region_name'] = init_regions.to_region(i.get('region_id'))
        return build_result(APIStatus.Ok, data=role_list, count=data.get('count', 0)), HTTPStatus.Ok
