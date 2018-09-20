from server.cache_data import init_regions
from server.meta.decorators import make_decorator
from server.status import make_resp, APIStatus, HTTPStatus


class RootManagement(object):

    @staticmethod
    @make_decorator
    def get_result(data):
        city_manager_list = data.get('city_manager_list')
        for detail in city_manager_list:
            if not detail['role_name']:
                detail['role_name'] = '无角色'

            if detail.get('is_deleted') == 0:
                detail['status'] = '启用'
            elif detail.get('is_deleted') == 1:
                detail['status'] = '禁用'
            detail.pop('is_deleted')

        return make_resp(APIStatus.Ok, data=city_manager_list, count=data.get('count', 0)), HTTPStatus.Ok


class RootRoleManagement(object):

    @staticmethod
    @make_decorator
    def get_result(data):
        role_list = data.get('role_list')
        for i in role_list:
            if i['region_id'] == 1:
                i['region_name'] = '全国'
            elif i['region_id'] == 2:
                i['region_name'] = '区镇'
            elif i['region_id'] == 3:
                i['region_name'] = '网点'
            else:
                i['region_name'] = init_regions.to_region(i.get('region_id'))

            if i['type'] == 1:
                i['type_name'] = '管理员'
            elif i['type'] == 2:
                i['type_name'] = '区镇合伙人'
            elif i['type'] == 3:
                i['type_name'] = '网点管理员'
            elif i['type'] == 4:
                i['type_name'] = '城市经理'

        return make_resp(APIStatus.Ok, data=role_list, count=data.get('count', 0)), HTTPStatus.Ok
