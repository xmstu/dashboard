import time

from flask_restful import abort

from server import log
from server.cache_data import init_regions
from server.meta.decorators import make_decorator, Response
from server.meta.session_operation import SessionOperationClass
from server.status import HTTPStatus, make_resp, APIStatus
from server.utils.constant import today_start_time
from server.utils.extend import compare_time
from server.utils.role_regions import get_role_regions


class TransportRadar(object):

    @staticmethod
    @make_decorator
    def check_params(params):
        try:
            if not SessionOperationClass.check():
                abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='请登录'))
            params['start_time'] = int(params.get('start_time', None) or today_start_time)
            params['end_time'] = int(params.get('end_time', None) or time.time())
            params['region_id'] = int(params.get('region_id', None) or 0)
            params['from_city_id'] = int(params.get('from_city_id', None) or 0)
            params['from_county_id'] = int(params.get('from_county_id', None) or 0)
            params['to_city_id'] = int(params.get('to_city_id', None) or 0)
            params['to_county_id'] = int(params.get('to_county_id', None) or 0)

            # 当前权限下所有地区
            params['region_id'] = get_role_regions(params['region_id'])

            if not compare_time(params['start_time'], params['end_time']):
                abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='时间参数有误'))

            return Response(params=params)

        except Exception as e:
            log.error('请求参数有误:{}'.format(e), exc_info=True)
            abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='请求参数有误'))


class TransportList(object):

    @staticmethod
    @make_decorator
    def check_params(page, limit, params):
        try:
            if not SessionOperationClass.check():
                abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='请登录'))
            # 校验参数并赋予默认值
            params['page'] = (page - 1) * limit
            params['limit'] = limit
            params['from_city_id'] = int(params.get('from_city_id', None) or 0)
            params['to_city_id'] = int(params.get('to_city_id', None) or 0)
            params['start_time'] = int(params.get('start_time', None) or today_start_time)
            params['end_time'] = int(params.get('end_time', None) or time.time())
            params['calc_town'] = int(params.get('calc_town', None) or 0)

            params['region_id'] = get_role_regions(0)
            if params['region_id'] == 0:
                if not params['from_city_id'] and not params['to_city_id']:
                    params['from_city_id'] = params['to_city_id'] = 440100
            else:
                if len(params['region_id']) == 1 and init_regions.get_current_region_level(params['region_id'][0]) == 2:
                    params['from_city_id'] = params['to_city_id'] = int(params['region_id'][0])
                else:
                    region_level_list = [{"region_id": i, "level": init_regions.get_current_region_level(i)} for i in
                                         params['region_id']]
                    highest_level_region = max(region_level_list, key=lambda k: k["level"])
                    highest_region = highest_level_region["region_id"]
                    highest_level = highest_level_region["level"]
                    if highest_level != 2:
                        highest_region = init_regions.get_parent_city(highest_region)
                    if not params['from_city_id'] and not params['to_city_id']:
                        params['from_city_id'] = params['to_city_id'] = highest_region

            # 校验时间
            if not compare_time(params['start_time'], params['end_time']):
                abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='筛选时间参数有误'))

            return Response(params=params)

        except Exception as e:
            log.error('error:{}'.format(e), exc_info=True)
            abort(HTTPStatus.BadRequest, **make_resp(status=APIStatus.BadRequest, msg='参数非法'))
